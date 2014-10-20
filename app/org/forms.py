# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms import ValidationError
from ..models import Organization


class RegistrationForm(Form):
    cellphone = StringField('Email', validators=[DataRequired(),
                                                 Length(11, 11)])
    captcha = StringField('Captcha', validators=[DataRequired,
                                                 Length(6, 6)])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])

    #def validate_cellphone(self, field):
    #    if Organization.query.filter_by(cellphone=field.data).first():
    #        raise ValidationError('Cellphone already registered.')


# TODO: cellphone regexp validator

class OrganizationForm2(Form):
    pass


class OrganizationForm3(Form):
    pass
