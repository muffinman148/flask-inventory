from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, PrintLabelForm, InventoryForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Items, Measurements
import printlabel as pl

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home Page', posts=posts)

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
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/printLabel', methods=['GET', 'POST'])
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
def inventory():
    form = InventoryForm()
    # if form.validate_on_submit(): # Checks form submission syntax validity
    if "submit" in request.form: # Checks form submission syntax validity
        item = Items.query.filter_by(ItemCode=form.itemCode.data).first()
        measurement = Measurements.query.filter_by(partNumber=form.itemCode.data).first()

        # Checks if part number field is correct
        if item is None: # Fail
            flash('No input. Please input a part number.')
            return redirect(url_for('inventory'))
        elif measurement is None: # Success
            flash('No previous measurements found for, ' + item.ItemCodeDesc + '.')
            return redirect(url_for('inventory'))
        else:
            flash('The last count was: ' + str(measurement.partCount) + '.')
            flash('Place item on the scale.')
            # flash('Printing Label ' + form.itemCode.data + '.' + item.ItemCodeDesc)
            # pl.sendPrintData(item)
    elif "weighItem" in request.form:
        flash('Place item onto scale.')
        # db.session.add(user)
        # db.session.commit()

    return render_template('inventory.html', title='Inventory', form=form)
