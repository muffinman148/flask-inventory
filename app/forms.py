from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Items, Measurements

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class PrintLabelForm(FlaskForm):
    itemCode = StringField('Part Number', validators=[DataRequired()])
    submit = SubmitField('Print Label')

    def validate_itemCode(self, itemCode):
        item = Items.query.filter_by(ItemCode=itemCode.data).first()
        if item is None:
            raise ValidationError('Item not found on record. Label cannot be printed.')

class InventoryForm(FlaskForm):
    itemCode = StringField('Part Number', validators=[DataRequired()])
    submit = SubmitField('Submit')
    weighItem = SubmitField('Weigh Item')

    def validate_itemCode(self, itemCode):
        item = Items.query.filter_by(ItemCode=itemCode.data).first()
        if item is None:
            raise ValidationError('Item not found on record.')

    def validate_measurements(self, itemCode):
        measurement = Measurements.query.filter_by(partNumber=itemCode.data).first()
        if measurement is None:
            raise ValidationError('No measurements on record.')
