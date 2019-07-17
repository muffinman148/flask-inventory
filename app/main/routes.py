"""
This file handles the Views for the inventory system. 
"""

from flask import render_template, flash, redirect, url_for, \
        request, jsonify, session, send_from_directory, current_app
from app import create_app, db
from app.tools import reverse_readline
from app.main.forms import PrintLabelForm, InventoryForm
from flask_login import current_user,  login_required
#  from flask_socketio import send
from app.models import *
from app.errors import *
import app.printlabel as pl
# import app.scale as s python 2.7 scale implementation
from app.decorator import requires_access_level
import os 
import logging
from logging.handlers import RotatingFileHandler
from app.main import bp
from datetime import date
import subprocess

# TODO Fix the following hack.
# The app needs to be called for logging to work, but will add multiple
# handlers. If different handlers are added/used in the future, you can change
# the 'app.logger.handlers.pop()' to 'app.logger.removeHandlers($INSERT_HANDLER)'
app = create_app()
while app.logger.handlers:
         app.logger.handlers.pop()

@bp.route('/favicon.ico') 
def favicon(): 
    """Returns favicon for all pages."""

    return send_from_directory(os.path.join(current_app.root_path, 'static'),\
            'favicon.ico', mimetype='image/vnd.microsoft.icon')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    """Returns the home page."""

    with open("logs/inventory.log", "r") as f:
        logs = "LOG FILE ENTRIES\n"
        lines = reverse_readline("logs/inventory.log")
        for line in lines:
            logs += line + "\n"

    state = Inventory.query.filter(Inventory.beginDate, Inventory.endDate == None).first()

    if request.method == 'POST':
        flash("Progress has updated to: " + str(progress), "info")
    elif state:
        progress = state.currentState
    else:
        progress = 0

    return render_template('index.html', title='Home Page', logs=logs, progress=progress)

@bp.route('/updateProgress', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def updateProgress():
    """Updates Inventory Progress."""

    # Query for Latest Open Inventory
    state = Inventory.query.filter(Inventory.beginDate, Inventory.endDate == None).first()

    if state:
        progress = state.currentState
        progress += 1 # Advance Inventory Stage

        if progress <= 4: # Continue to next Inventory Stage

            if progress == 2: # Clear Database
                flash("TODO Finish Clear Database")
                # Do the Following SQL: INV1

                # Raw SQL Test
                #  with engine.connect() as con:
                #      rs = con.execute('SELECT * FROM items')

                #      for row in rs:
                #          print row

                #  UPDATE Node_RPI_InvCount SET InvDate = NULL, TotalPieces = 0;
                #  DELETE FROM `Node_RPI_InvCount` WHERE TotalPieces = 0 AND
                #  (PieceWeight = 0 OR PieceWeight = NULL);

            elif progress == 3: # Progress Check
                flash("TODO Finish Progress Check")
                # Do the Following SQL: INV2

                #  UPDATE `federated_IM_Physical`
                #  INNER JOIN `Node_RPI_InvCount` ON (
                #          `federated_IM_Physical`.`ItemCode` =
                #          `Node_RPI_InvCount`.`ItemCode` ) 
                #  SET `QuantityCounted` = `TotalPieces`,
                #  `DateUpdated` = STR_TO_DATE(DATE_FORMAT(`InvDate`,
                #      '%Y-%m-%d'),'%Y-%m-%d'),
                #  `TimeUpdated` = TIME_TO_SEC( DATE_FORMAT(InvDate,'%H:%i:%s') )
                #  / (60*60) 
                #  WHERE
                #      `InvDate` > "2017-01-01 00:00:00";

                flash("TODO Finish Progress Check")
                # Do the Following SQL: INV3

                # /* Still need to Inventory the following items */ 
		#  SELECT
		#      p.BinLocation AS Location,
		#      p.ProductLine AS ProdLine,
		#      p.ItemCode AS Item,
		#      p.ItemCodeDesc AS Description,
		#      round( p.QuantityOnHand ) AS In_Sage,
		#      p.StandardUnitOfMeasure AS Unit,
		#      "" AS "Count",
		#      "" AS "WIP",
		#      p.ItemCode AS Item,
		#      CONCAT( "$", round( p.QuantityOnHand * i.AverageUnitCost ) ) AS "Value",
		#      i.LastSoldDate 
		#  FROM
		#      rpi_im_physical p
		#      LEFT JOIN `rpi_inv_ci_item` i ON p.ItemCode = i.ItemCode 
		#  WHERE
		#      ( p.QuantityOnHand > 0 OR i.LastSoldDate > CURDATE( ) - INTERVAL 4 YEAR ) 
		#      AND p.QuantityCounted = 0 
		#      AND p.ProductLine IN ( "RM", "RMX", "EQ" )
		#      AND i.InactiveItem = "N" 
		#  ORDER BY
		#      p.BinLocation,
		#      p.ItemCode

                # TODO Add Copy INV3 output to file and print nicely

            elif progress == 4: 
                flash("TODO Create method to copy file to vm7.")
                # Do the Following SQL: INV4

                #  SELECT
                #      i.WarehouseCode,
                #      i.ItemCode ,
                #      IFNULL(c.TotalPieces,IF(i.QuantityOnHand=0,0,9999)) AS QuantityCounted
                #  FROM
                #      `Node_RPI_InvCount` c
                #  RIGHT JOIN `federated_IM_Physical` i ON c.ItemCode = i.ItemCode
                #  WHERE

                #  i.ProductLine = "RM" || i.ProductLine = "RMX" || i.ProductLine = "EQ"

                #  ORDER BY
                #      i.ItemCode ASC

                #  Copy results (Tab Separated Values (Data Only)) to Excel and then save as CSV file to vm7/e$/Import/inventory.csv 
                #  Use Sage Visual Integrator to import the data into IM_Physical.

                # TODO Potentially add api to interface with SAGE

            state.currentState = progress
            db.session.commit()
            app.logger.info("%s has continued inventory to stage %s at %s.", 
                    current_user.username, progress, date.today())

        elif progress > 4: # End Inventory
            state.currentState = progress
            state.endDate = date.today()
            db.session.commit()
            app.logger.info('User "%s" has closed Inventory at %s.',
                    current_user.username, state.endDate)

    else: # State is undefined
        flash("Failure to find latest Inventory.", "error")

        return redirect(url_for('errors.internal_error'))

    return jsonify(progress=progress)

@bp.route('/clearLogs', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def clearLogs():
    """Clears current logs."""

    p = subprocess.Popen(["> logs/inventory.log"], shell=True, stdout=subprocess.PIPE)
    if p.returncode != 0:
        # TODO Finish this error flashing for user
        flash("Logs could not be cleared.", "error")

        return jsonify(success=False)

    return jsonify(success=True)

@bp.route('/startProgress', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def startProgress():
    """Starts Inventory Progress."""

    # Start New Inventory
    newInventory = Inventory(user=current_user.id, 
                             currentState=1,
                             beginDate=date.today(),
                             endDate=None)
    db.session.add(newInventory)
    db.session.commit()

    app.logger.info("%s has started inventory at %s.",
            current_user.username, date.today())

    print("TODO Finish Clear Database")
    # Do the Following SQL: INV1

    #  UPDATE Node_RPI_InvCount SET InvDate = NULL, TotalPieces = 0;
    #  DELETE FROM `Node_RPI_InvCount` WHERE TotalPieces = 0 AND
    #  (PieceWeight = 0 OR PieceWeight = NULL);


    return jsonify(success=True)

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
            #  app.logger.info('"' + str(current_user.username) + '"' + ' has printed a label for item ' + 
            #          form.itemCode.data + ' has been printed.')
            app.logger.info('%s has printed a label for item %s has been printed.',
                    current_user.username, form.itemCode.data)

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
        #  app.logger.info('"' + str(current_user.username) + '"' + " prepping weighing of item " + 
        #          form.itemCode.data)
        app.logger.info("%s prepping weighing of item %s.",
                current_user.username, form.itemCode.data)

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
            #  app.logger.info('"' + str(current_user.username) + '"' + " created new measurement for item: " + 
            #          form.itemCode.data)
            app.logger.info("%s created new measurement for item: %s",
                    current_user.username, form.itemCode.data)

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
        #  app.logger.info('"' + str(current_user.username) + '"' + ' has add item ' + 
        #          form.itemCode.data + ' to the Items table.')
        app.logger.info("%s has add item %s to the Items table. ",
                current_user.username, form.itemCode.data)
    else:
        #  app.logger.info('"' + str(current_user.username) + '"' + ' was not able add item ' + 
        #          form.itemCode.data + ' to the Items table.')
        app.logger.info("%s was not able to add item %s to the Items table. ",
                current_user.username, form.itemCode.data)
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
        #  app.logger.error('Illegal mode: "' + mode + '" Contact administrator.')
        app.logger.error('Illegal mode: "%s" Contact administrator.', 
                mode)

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
        #  app.logger.info('"' + str(current_user.username) + '"' + ' is taring ' + 
        #          str(item) + ' with container weight of: ' + str(weight))
        app.logger.info("%s is taring %s with container weight of: %s",
                current_user.username, item, weight)

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
        #  app.logger.info('"' + str(current_user.username) + '"' + ' has counted ' + 
        #          str(item) + ' with a count of ' + str(weight))
        app.logger.info("%s has counted %s with a count of %s.",
                current_user.username, item, weight)

    elif mode is None:
        flash('Session mode is not passed. Session is corrupt or navigated to\
                prematurely.', 'danger')
        app.logger.error('Session mode is not passed. Session is corrupt or navigated to prematurely.')

        return redirect(url_for('main.inventory'))

    else:
        flash('Illegal mode: "' + mode + '" Contact administrator.', 'danger')
        db.session.rollback()
        #  app.logger.error('Illegal mode: "' + mode + '" Contact administrator.')
        app.logger.error('Illegal mode: "%s" Contact administrator.', 
                mode)

    return jsonify(weight=weight)
