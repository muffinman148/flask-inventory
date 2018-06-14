"""
Defines all forms.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
        SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Items, Measurements
import re

class PrintLabelForm(FlaskForm):
    """Print label form used for validating and printing given part number
    values."""

    itemCode = StringField('Part Number', validators=[DataRequired()])
    submit = SubmitField('Print Label')

    def validate_itemCode(self, itemCode):
        item = Items.query.filter_by(ItemCode=itemCode.data).first()
        if item is None:
            raise ValidationError('Item not found on record. Label cannot be printed.')

class InventoryForm(FlaskForm):
    """Inventory form used for validating a given part number."""

    itemCode = StringField('Part Number', validators=[DataRequired()],
            render_kw={'autofocus': True})
    submit = SubmitField('Submit')

    def validate_itemCode(self, itemCode):
        """Checks to see if part number is in main table."""

        item = Items.query.filter_by(ItemCode=itemCode.data).first()
        if item is None:
            raise ValidationError('Item not found on record.')

    def validate_measurements(self, itemCode):
        """Checks to see if part number was recently measured."""

        measurement = Measurements.query.filter_by(partNumber=itemCode.data).first()
        if measurement is None:
            raise ValidationError('No measurements on record.')
