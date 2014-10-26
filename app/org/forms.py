# -*- coding: utf-8 -*-
import uuid
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField,\
    TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import ValidationError
from ..models import Organization, Type


class RegistrationForm(Form):
    cellphone = StringField('cellphone',
                            validators=[
                                DataRequired(u'必填'),
                                Length(11, 11, u'手机号码不符合规范')])
    captcha = StringField('Captcha', validators=[DataRequired(u'必填'),
                                                 Length(6, 6, u'验证码错误')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])

    def validate_cellphone(self, field):
        if Organization.query.filter_by(mobile=field.data).first():
            raise ValidationError('Cellphone already registered.')


# TODO: cellphone regexp validator

class DetailForm(Form):
    type_id = SelectField(coerce=int)
    name = StringField()
    profession_id = SelectField(coerce=int)
    property_id = SelectField(coerce=int)
    size_id = SelectField(coerce=int)
    contact = StringField()
    location_id = SelectField(coerce=int)
    address = StringField()
    intro = TextAreaField()


class CertificationForm(Form):
    certification = FileField(validators=[
        FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    photo = FileField(validators=[
        FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])


class LoginForm(Form):
    cellphone = StringField(validators=[DataRequired(), Length(11, 11)])
    password = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField()

class AddCourseForm(Form):
    name = StringField()
    age_id = SelectField(coerce=int)
    price = StringField()
    consult_time = StringField()
    is_tastable = BooleanField()

class ActivityForm(Form):
    name = StringField()
    age_id = SelectField()
    price = StringField()
    start_time = StringField()
    end_time = StringField()
    intro = StringField()
