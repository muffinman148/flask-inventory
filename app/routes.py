from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from app.forms import LoginForm, RegistrationForm, PrintLabelForm, \
    InventoryForm1, InventoryForm2
from flask_login import current_user, login_user, logout_user, login_required
# from app.models import User, Items, Measurements, UserTable
from app.models import *
import printlabel as pl
import scale as s
from decorator import requires_access_level

item = Items
measurement = Measurements


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home Page')

@app.route('/login', methods=['GET','POST'])
def login():
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
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(401)
def page_not_found(e):
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, \
                access=form.access.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User registered.')
        return redirect(url_for('users'))
    return render_template('register.html', title='Register', form=form)

@app.route('/printLabel', methods=['GET', 'POST'])
@login_required
def printLabel():
    form = PrintLabelForm()
    if form.validate_on_submit(): # Checks form submission syntax validity
        item = Items.query.filter_by(ItemCode=form.itemCode.data).first()

        # Checks if part number field is correct
        if item is None:
            flash('No input. Please input a part number.')
            return redirect(url_for('printLabel'))
        else:
            flash('Printing Label ' + form.itemCode.data + '.' + item.ItemCodeDesc)
            pl.sendPrintData(item)

    return render_template('printLabel.html', title='Print Labels', form=form)

@app.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    form = InventoryForm1()
    # if form.validate_on_submit(): # Checks form submission syntax validity
    if "submit" in request.form: # Checks form submission syntax validity
        item = Items.query.filter_by(ItemCode=form.itemCode.data).first()
        measurement = Measurements.query.filter_by(partNumber=form.itemCode.data).first()

        # Checks if part number field is correct
        if item is None: # No input for the field
            flash('Item not on file.')
            return redirect(url_for('inventory'))
        elif measurement is None: # No current measurements available
            flash('No previous measurements found for, ' + item.ItemCodeDesc + '.')
            flash('Place empty container on scale.')
            # while container is not containerChange and keyboardIdle:
            #     do await item data input
        else: # Generate Item Report
            flash('Place bin to be counted.')
            # User clicks "Weigh Item"
            
    return render_template('inventory.html', title='Inventory', form=form)

@app.route('/weighItem', methods=['GET', 'POST'])
@login_required
def weighItem():
    weight = s.runScale("getWeight", 0)
    print(weight)
    print(item.ItemCodeDesc)
    print(measurement.pieceWeight)
    return jsonify(weight=weight)

@app.route('/users', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def users():
    """ Creates admin user's panel."""
    table = UserTable(User.query.all())
    print("We did it!")
    return render_template('users.html', title='User\'s table', table=table)
