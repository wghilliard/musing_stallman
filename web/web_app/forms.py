from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators


class RegistrationForm(FlaskForm):
    username = StringField('Desired Username', [validators.Length(min=4, max=25),
    validators.Regexp('^[a-z0-9_.-]+$', message = "Username can only contain lowercase letters, numbers, -, _, and .") ])
    full_name = StringField('Full Name', [validators.Length(min=2, max=35)])
    email = StringField('Email Address', [validators.Email()])
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])



