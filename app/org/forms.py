# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms import ValidationError
from ..models import User


class OrganizationForm1(Form):
    cellphone = StringField('Email', validators=[DataRequired(),
                                                 Length(11, 11)])
    captcha = StringField('Captcha', validators=[DataRequired,
                                                 Length(6, 6)])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_cellphone(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


# TODO: cellphone regexp validator

class OrganizationForm2(Form):
    cellphone = StringField('Email', validators=[DataRequired(),
                                                 Length(11, 11)])
    captcha = StringField('Captcha', validators=[DataRequired,
                                                 Length(6, 6)])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_cellphone(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class OrganizationForm3(Form):
    cellphone = StringField('Email', validators=[DataRequired(),
                                                 Length(11, 11)])
    captcha = StringField('Captcha', validators=[DataRequired,
                                                 Length(6, 6)])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_cellphone(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
