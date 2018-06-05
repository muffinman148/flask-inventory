"""
Defines authentication forms.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
        SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
import re
from app.auth import bp

class LoginForm(FlaskForm):
    """Login form used for user authentication."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
