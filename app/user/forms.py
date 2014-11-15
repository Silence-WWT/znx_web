# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError
from ..models import User
from ..utils.validator import Captcha, EmptyEmail


# TODO: add telephone number.
class LoginForm(Form):
    username = StringField(validators=[DataRequired(), Length(4, 16)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')


class RegistrationForm(Form):
    username = StringField('username',
                           validators=[DataRequired(u'必填'),
                                       Length(4, 16, u'用户名长度不符合要求')])
    cellphone = StringField('cellphone',
                            validators=[
                                DataRequired(u'必填'),
                                Length(11, 11, u'手机号码不符合规范')])
    captcha = StringField('cpatcha', validators=[Captcha('user', 'cellphone')])
    email = StringField('Email', validators=[EmptyEmail(u'邮箱不符合规范')])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(6, 20, u'密码长度不符合规范'),
        EqualTo('password2', message=u'密码不一致')])
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


class ResetPasswordForm(Form):
    cellphone = StringField('cellphone',
                            validators=[
                                DataRequired(u'必填'),
                                Length(11, 11, u'手机号码不符合规范')])
    captcha = StringField('cpatcha', validators=[Captcha('user', 'cellphone')])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(6, 20, u'密码长度不符合规范'),
        EqualTo('password2', message=u'密码不一致')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])

    def validate_cellphone(self, field):
        if not User.query.filter_by(mobile=field.data).first():
            raise ValidationError(u'手机号未经注册')
