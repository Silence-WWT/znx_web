# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError
from ..models import User


# TODO: add telephone number.
class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

class OrganizationForm1(Form):
    cellphone = StringField('Email', validators=[DataRequired(),
                                                 Length(11, 11) ])
    captcha = StringField('Captcha', validators=[DataRequired,
                                                 Length(6,6)])
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
                                                 Length(11, 11) ])
    captcha = StringField('Captcha', validators=[DataRequired,
                                                 Length(6,6)])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_cellphone(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class OrganizationForm3(Form):
    cellphone = StringField('Email', validators=[DataRequired(),
                                                 Length(11, 11) ])
    captcha = StringField('Captcha', validators=[DataRequired,
                                                 Length(6,6)])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_cellphone(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
