from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators


class RegistrationForm(FlaskForm):
    username = StringField('Desired Username', [validators.Length(min=4, max=25)])
    full_name = StringField('Full Name', [validators.Length(min=2, max=35)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
