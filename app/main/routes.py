"""
This file handles the Views for the inventory system. 
"""

from flask import render_template, flash, redirect, url_for, \
        request, jsonify, session, send_from_directory, current_app
from app import db
from app.main.forms import PrintLabelForm, InventoryForm
from flask_login import current_user,  login_required
from app.models import *
from app.errors import *
import app.printlabel as pl
# import app.scale as s python 2.7 scale implementation
from app.decorator import requires_access_level
import os 
import logging
from logging.handlers import RotatingFileHandler
from app.main import bp

@bp.route('/favicon.ico') 
def favicon(): 
    """Returns favicon for all pages."""

    return send_from_directory(os.path.join(current_app.root_path, 'static'),\
            'favicon.ico', mimetype='image/vnd.microsoft.icon')

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    """Returns the home page."""

    with open("logs/inventory.log", "r") as f:
        logs = f.read()

    return render_template('index.html', title='Home Page', logs=logs)

@bp.route('/printLabel', methods=['GET', 'POST'])
@login_required
def printLabel():
    """Print label form that allows user to print to Brother QL-720NW
    printer."""

    form = PrintLabelForm()
    if form.validate_on_submit(): # Checks form submission syntax validity
        item = Items.query.filter_by(ItemCode=form.itemCode.data).first()

        # Checks if part number field is correct
        if item is None:
            flash('No input. Please input a part number.', 'warning')
            return redirect(url_for('main.printLabel'))
        else:
            flash('Printing Label ' + form.itemCode.data + '.' + item.ItemCodeDesc, 'success')
            if os.environ['FLASK_ENV'] != 'development':
                pl.sendPrintData(item)
            app.logger.info('"' + str(current_user.username) + '"' + ' has printed a label for item ' + 
                    form.itemCode.data + ' has been printed.')

    return render_template('printLabel.html', title='Print Labels', form=form)

@bp.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    """Inventory form to check if item is on file. """

    # TODO Fix form logic
    form = InventoryForm()
    
    # Clear Old Inventory Session
    # session.pop('mode', None)

    if "submit" in request.form: # Checks form submission syntax validity
        item = Items.query.filter_by(ItemCode=form.itemCode.data).first()
        measurement = Measurements.query.filter_by(partNumber=form.itemCode.data).first()
        app.logger.info('"' + str(current_user.username) + '"' + " prepping weighing of item " + 
                form.itemCode.data)

        # Checks if part number field is correct
        if item is None: # No input for the field
            session['item'] = form.itemCode.data
            flash('Item: ' + str(form.itemCode.data) + ' not on file.', 'warning')
            return redirect(url_for('main.inventory'))

        elif measurement is None: # No current measurements available
            session.pop('item', None)
            flash('No previous measurements found for, ' + form.itemCode.data + '.', 'warning')
            flash('Place empty container on scale.', 'info')
            mode = "tare"

            # Create new Measurement for Item
            newMeasurement = Measurements(partNumber=form.itemCode.data)
            db.session.add(newMeasurement)
            db.session.commit()
            app.logger.info('"' + str(current_user.username) + '"' + " created new measurement for item: " + 
                    form.itemCode.data)

        elif measurement.tareWeight == 0 or measurement.tareWeight is None: # Measurement and previous tareWeight exists
            flash('Place empty container on scale.', 'info')
            mode = "tare"

        else: # Generate Item Report
            flash('Place bin to be counted.', 'info')
            mode = "count"

        # Set session mode
        session['mode'] = mode
        session['item'] = form.itemCode.data

        return redirect(url_for('main.inventoryItem', item=form.itemCode.data, mode=mode))
            
    return render_template('inventory.html', title='Inventory', form=form)

@bp.route('/inventory/addItem', methods=['POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def addItem():
    """Returns json of newly added item."""

    item = session.get('item', None)
    if(item is not None):
        newItem = Items(ItemCode=item)
        db.session.add(newItem)
        db.session.commit()
        app.logger.info('"' + str(current_user.username) + '"' + ' has add item ' + 
                form.itemCode.data + ' to the Items table.')
    else:
        app.logger.info('"' + str(current_user.username) + '"' + ' was not able add item ' + 
                form.itemCode.data + ' to the Items table.')
        return internal_error(item)

    return jsonify(item=item) # TODO Pass confirmation instead?

@bp.route('/inventory/<mode>-<item>', methods=['GET', 'POST'])
@login_required
def inventoryItem(item, mode):
    """Returns item's inventory page.

    Args:
        item (str): Part number name.
        mode (str): Mode that determines what method is performed on data.
    """

    flash('Current mode is: ' + mode, 'info')
    if mode == "tare" or "count": # User is weighing container
        table = MeasurementsTable(Measurements.query.filter_by(partNumber=item))
    else: # Illegal mode passed
        flash('Illegal mode: "' + mode + '" Contact administrator.', 'danger')
        app.logger.error('Illegal mode: "' + mode + '" Contact administrator.')

        return redirect(url_for('main.inventory'))

    return render_template('item.html', title=item, item=item, mode=mode, table=table)

@bp.route('/weighItem', methods=['GET', 'POST'])
@login_required
def weighItem():
    """Returns json of weight of an item."""

    # Initializes Session Variables
    mode = session.get('mode', None)
    item = session.get('item', None)
    
    # TODO Add new implementation for Fairbanks scale
    # Retrieves Scale Data
    # weight = s.runScale("getWeight", 0)

    # This is for TESTING
    print("Scale weight is: " + str(weight))
    weight = 0.0
    # End TESTING

    measurementObject = Measurements.query.filter_by(partNumber=item).first()

    # Tare Conditions 
    # ---------------
    # User has submitted an item value that does not have a tare weight
    if mode == 'tare':
        # tareWeight=weight
        measurementObject.tareWeight = weight
        db.session.commit()
        session['mode'] = 'count'
        app.logger.info('"' + str(current_user.username) + '"' + ' is taring ' + 
                str(item) + ' with container weight of: ' + str(weight))

    # Count Conditions 
    # ----------------
    # User has submitted an item value that contains tare weight. Count should
    # be accessible regardless if count data already exists in the event of a
    # need for resubmission of data.
    elif mode == 'count':
        # totalWeight=weight
        measurementObject.totalWeight = weight
        # totalWeight=-tareWeight
        measurementObject.totalWeight -= float(measurementObject.tareWeight)
        db.session.commit()
        app.logger.info('"' + str(current_user.username) + '"' + ' has counted ' + 
                str(item) + ' with a count of ' + str(weight))

    elif mode is None:
        flash('Session mode is not passed. Session is corrupt or navigated to\
                prematurely.', 'danger')
        app.logger.error('Session mode is not passed. Session is corrupt or navigated to prematurely.')

        return redirect(url_for('main.inventory'))

    else:
        flash('Illegal mode: "' + mode + '" Contact administrator.', 'danger')
        db.session.rollback()
        app.logger.error('Illegal mode: "' + mode + '" Contact administrator.')

    return jsonify(weight=weight)
