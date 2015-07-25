# -*- encoding: utf8 -*-

from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField, StringField
from wtforms.validators import Required, EqualTo, Email, Length

class LoginForm(Form):
    email = TextField('Email address', [Length(min=6, max=120), Required(), Email()])
    password = PasswordField('Password', [Length(min=8, max=20), Required()])

class RegistrationFrom(LoginForm):
    name = StringField('Full Name', [
        Required(), Length(min=2, max=10)
        ])
    confirm = PasswordField('Repeat password', [
        Length(min=8, max=20), Required(),
        EqualTo('password', message='Passwords must match')
        ])
    tos = BooleanField('I accept the Terms of Service', [Required()])
    recaptcha = RecaptchaField()
