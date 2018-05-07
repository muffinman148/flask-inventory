from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
        SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Items, Measurements
import re

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    access = SelectField(u'User Access Level', \
            choices=[('guest','guest'), ('user','user'), ('admin','admin')])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register User')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        if not re.match("^\S+@.+\..+", email.data): # Extremely loose regex
            raise ValidationError('Invalid email address.')

class PrintLabelForm(FlaskForm):
    itemCode = StringField('Part Number', validators=[DataRequired()])
    submit = SubmitField('Print Label')

    def validate_itemCode(self, itemCode):
        item = Items.query.filter_by(ItemCode=itemCode.data).first()
        if item is None:
            raise ValidationError('Item not found on record. Label cannot be printed.')

class InventoryForm1(FlaskForm):
    itemCode = StringField('Part Number', validators=[DataRequired()],
            render_kw={'autofocus': True})
    submit = SubmitField('Submit')

    def validate_itemCode(self, itemCode):
        item = Items.query.filter_by(ItemCode=itemCode.data).first()
        if item is None:
            raise ValidationError('Item not found on record.')

    def validate_measurements(self, itemCode):
        measurement = Measurements.query.filter_by(partNumber=itemCode.data).first()
        if measurement is None:
            raise ValidationError('No measurements on record.')

class InventoryForm2(FlaskForm):
    itemCode = StringField('Part Number', validators=[DataRequired()],
            render_kw={'autofocus': True})
    weighItem = SubmitField('Weigh Item')
