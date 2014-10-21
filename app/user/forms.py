# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError
from ..models import User


# TODO: add telephone number.
class LoginForm(Form):
    username = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')


class RegistrationForm(Form):
    username = StringField('username',
                           validators=[DataRequired(),
                                       Length(6,64, u'用户名长度不符合要求')])
    cellphone = StringField('cellphone',
                            validators=[
                                DataRequired(u'必填'),
                                Length(11, 11, u'手机号码不符合规范')])
    email = StringField('Email', validators=[Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])

    confirmed = BooleanField()

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已经被占用')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已经被注册')

    def validate_cellphone(self, field):
        if User.query.filter_by(cellphone=field.data).first():
            raise ValidationError(u'手机号已经被注册')

    def validate_confirmed(self, field):
        if field.data == False:
            raise ValidationError(u'请确认协议')
