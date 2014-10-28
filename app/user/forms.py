# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError
from ..models import User
from ..utils.validator import Captcha


# TODO: add telephone number.
class LoginForm(Form):
    username = StringField(validators=[DataRequired(), Length(1, 64)])
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
    captcha = StringField('cpatcha', validators=[Captcha('user', 'cellphone')])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])

    confirmed = BooleanField()

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已经被占用')

    def validate_cellphone(self, field):
        if User.query.filter_by(mobile=field.data).first():
            raise ValidationError(u'手机号已经被注册')

    def validate_confirmed(self, field):
        if field.data == False:
            raise ValidationError(u'请确认协议')
