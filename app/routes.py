"""
This file handles the Views for the inventory system. 
"""

from flask import render_template, flash, redirect, url_for, \
        request, jsonify, session, send_from_directory
from app import app, db
from app.forms import LoginForm, RegistrationForm, PrintLabelForm, \
    InventoryForm1, InventoryForm2
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
import printlabel as pl
import scale as s
from decorator import requires_access_level
from pprint import pprint
import os 

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'),\
            'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
@app.route('/index')
@login_required
def index():
    """Returns the home page."""

    return render_template('index.html', title='Home Page')

@app.route('/login', methods=['GET','POST'])
def login():
    """Returns the login page. This page authenticates users."""

    if current_user.is_authenticated: # Redirects logged in users
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit(): # Checks form submission syntax validity
        user = User.query.filter_by(username=form.username.data).first()

        # Checks if username field is empty or password is correct
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))

        # User logged in successfully
        login_user(user, remember=form.remember_me.data)

        # Logs User into original inputted URL
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    """Logs user out. Redirects to login page."""

    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(401)
def page_not_found(e):
    """Redirects users without proper access to login page."""

    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def register():
    """Allows an admin user the ability to add other users the system."""

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, \
                access=form.access.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User registered.', 'success')
        return redirect(url_for('users'))
    return render_template('register.html', title='Register', form=form)

@app.route('/printLabel', methods=['GET', 'POST'])
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
            return redirect(url_for('printLabel'))
        else:
            flash('Printing Label ' + form.itemCode.data + '.' + item.ItemCodeDesc, 'success')
            pl.sendPrintData(item)

    return render_template('printLabel.html', title='Print Labels', form=form)

@app.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    """Inventory form to check if item is on file. """

    # TODO Fix form logic
    form = InventoryForm1()
    # if form.validate_on_submit(): # Checks form submission syntax validity
    mode = ""
    if "submit" in request.form: # Checks form submission syntax validity
        item = Items.query.filter_by(ItemCode=form.itemCode.data).first()
        measurement = Measurements.query.filter_by(partNumber=form.itemCode.data).first()

        # Checks if part number field is correct
        if item is None: # No input for the field
            flash('Item not on file.', 'warning')
            state = "noitem"
            return redirect(url_for('inventory', state=state))
        elif measurement is None: # No current measurements available
            flash('No previous measurements found for, ' + item.ItemCodeDesc + '.', 'warning')
            flash('Place empty container on scale.', 'info')
            mode = "tare"
            return redirect(url_for('inventoryItem', item=form.itemCode.data, mode=mode))
        else: # Generate Item Report
            # User clicks "Weigh Item"
            flash('Place bin to be counted.', 'info')
            mode = "count"
            # weight = s.runScale("getWeight", 0)
            return redirect(url_for('inventoryItem', item=form.itemCode.data, mode=mode))
            
    return render_template('inventory.html', title='Inventory', form=form)

@app.route('/inventory/<mode>-<item>', methods=['GET', 'POST'])
@login_required
def inventoryItem(item, mode):
    """Returns item's inventory page.

    Args:
        item (str): Part number name.
        mode (str): Mode that determines what method is performed on data.
    """

    flash('Current mode is: ' + mode, 'info')
    # TODO Finish logic for tare and count methods
    if mode == "tare":
        weight = session.get('weight', None)
        if weight:
            flash("We have the weight: " + str(weight) + ".", 'info')
        table = MeasurementsTable(Measurements.query.filter_by(partNumber=item))
        return render_template('item.html', title=item, item=item, mode=mode, table=table)
    elif mode == "count":
        table = MeasurementsTable(Measurements.query.filter_by(partNumber=item))
        return render_template('item.html', title=item, item=item, mode=mode, table=table)
    else:
        flash('Illegal mode: "' + mode + '" Contact administrator.', 'danger')
        return redirect(url_for('inventory'))

@app.route('/weighItem', methods=['GET', 'POST'])
@login_required
def weighItem():
    """Returns json of weight of an item."""

    weight = s.runScale("getWeight", 0)
    # part = Measurements(partNumber=item.partNumber, pieceWeight=weight)
    # db.session.update().values(part)
    print( "The session weight is: " + str(session['weight']))
    return jsonify(weight=weight)

@app.route('/users', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def users():
    """Creates admin user's panel."""

    sort = request.args.get('sort', 'username')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    table = UserTable(User.get_sorted_by(sort, reverse), 
            sort_by=sort, 
            sort_reverse=reverse)

    # table = UserTable(User.query.all())
    return render_template('users.html', title='User\'s table', table=table)

@app.route('/users/delete-<username>', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def deleteUser(username):
    """Deletes user if not current user
    
    Args:
        username (obj): Username object to delete
    """

    if str(username) in str(current_user):
        flash('You cannot delete your own account!', 'warning')
        return redirect(url_for('users'))
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()

    flash('User deleted!', 'success')
    return redirect(url_for('users'))
