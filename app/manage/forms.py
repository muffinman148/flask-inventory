"""
Defines user management forms.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
        SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Items, Measurements
import re

class RegistrationForm(FlaskForm):
    """Registration form used for registering users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    access = SelectField(u'User Access Level', \
            choices=[('guest','guest'), ('user','user'), ('admin','admin')])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register User')

    def validate_username(self, username):
        """Checks for duplicate username."""

        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """Checks for valid email convention."""

        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        if not re.match("^\S+@.+\..+", email.data): # Extremely loose regex
            raise ValidationError('Invalid email address.')

class EditProfileForm(FlaskForm):
    """Edit Profile form used for editing user information."""

    username = StringField('Username')
    email = StringField('Email')
    access = SelectField(u'User Access Level', \
            choices=[('guest','guest'), ('user','user'), ('admin','admin')])
    submit = SubmitField('Edit User')

    # TODO Add Form Validation for changed values only
    # def validate_username(self, username):
    #     """Checks for duplicate username."""

    #     user = User.query.filter_by(username=username.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different username.')

    # def validate_email(self, email):
    #     """Checks for valid email convention."""

    #     user = User.query.filter_by(email=email.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different email address.')
    #     if not re.match("^\S+@.+\..+", email.data): # Extremely loose regex
    #         raise ValidationError('Invalid email address.')

class ResetPasswordForm(FlaskForm):
    """Registration form used for registering users."""

    # username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
