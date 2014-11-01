# -*- coding: utf-8 -*-
import uuid
import time
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField,\
    SelectMultipleField, TextAreaField, BooleanField, RadioField, \
    DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import ValidationError
from ..models import Organization, Age, Class, Activity, OrganizationComment,\
    Time
from flask.ext.login import current_user
from ..utils.validator import Captcha
from ..utils.query import select_multi_checkbox


class RegistrationForm(Form):
    cellphone = StringField('cellphone',
                            validators=[
                                DataRequired(u'必填'),
                                Length(11, 11, u'手机号码不符合规范')])
    captcha = StringField('Captcha', validators=[DataRequired(u'必填'),
                                                 Length(6, 6, u'验证码错误'),
                                                 Captcha('org', 'cellphone')])
    password = PasswordField('Password', validators=[
        DataRequired(u'必填'),
        Length(6, 20, u'密码长度不符合规范'),
        EqualTo('password2', message=u'密码不一致')])
    password2 = PasswordField('Confirm password',
                              validators=[DataRequired(u'必填')])

    def validate_cellphone(self, field):
        if Organization.query.filter_by(mobile=field.data).first():
            raise ValidationError(u'手机号已被注册')


# TODO: cellphone regexp validator

class DetailForm(Form):
    type_id = SelectField(coerce=int)
    name = StringField('name', validators=[DataRequired(u'必填'),
                                           Length(1, 30, u'名字长度不符合规范')])
    profession_id = SelectField(coerce=int)
    property_id = SelectField(coerce=int)
    size_id = SelectField(coerce=int)
    contact = StringField('contact',
                          validators=[DataRequired(u'必填'),
                                      Length(1, 6, u'联系人长度不符合规范')])
    location_id = SelectField(coerce=int)
    address = StringField('address',
                          validators=[DataRequired(u'必填'),
                                      Length(1, 40, u'地址长度不符合规范')])
    intro = TextAreaField('intro',
                          validators=[DataRequired(u'必填'),
                                      Length(1, 140, u'简介长度不符合规范')])


class CertificationForm(Form):
    certification = FileField(validators=[
        FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    photo = FileField(validators=[
        FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])


class LoginForm(Form):
    cellphone = StringField(validators=[DataRequired(), Length(11, 11)])
    password = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField()


class CourseForm(Form):
    name = StringField('name',
                       validators=[
                           DataRequired(u'必填'),
                           Length(1, 30, u'长度不超过30个字符')])
    age_id = SelectField('age_id', coerce=int)
    price = IntegerField('price', validators=[DataRequired(u'必填')])
    consult_time = StringField('consult_time', validators=[
                               DataRequired(u'必填'),
                               Length(1, 20, u'长度不超过20字符')])
    days = IntegerField('days', validators=[DataRequired(u'必填')])
    is_tastable = RadioField('is_tastable', choices=[(1, 'yes'), (0, 'no')],
                             coerce=int)
    is_round = RadioField('is_round', choices=[(1, 'yes'), (0, 'no')],
                          coerce=int)
    intro = TextAreaField('intro', validators=[
        DataRequired(u'必填'),
        Length(1, 140, u'长度不超过140个字符')])
    class_time = SelectMultipleField('class_time',
                                     validators=[DataRequired(u'至少选一项')],
                                     coerce=int,
                                     widget=select_multi_checkbox)

    def create_choices(self):
        ages = Age.query.all()
        self.age_id.choices = [(age.id, age.age) for age in ages]
        self.class_time.choices = [(time.id, time.time)
                                   for time in Time.query.all()]

    def create_course(self):
        # TODO: check is org not user.
        # TODO: class time.
        course = Class(organization_id=current_user.id,
                       name=self.name.data,
                       age_id=self.age_id.data,
                       price=self.price.data,
                       consult_time=self.consult_time.data,
                       is_tastable=bool(self.is_tastable.data),
                       is_round=bool(self.is_round.data),
                       days=self.days.data,
                       intro=self.intro.data,
                       created=time.time())
        return course


class ActivityForm(Form):
    name = StringField('name')
    age_id = SelectField('age_id', coerce=int)
    price = StringField('prince')
    start_time = DateTimeField('start_time', format='%Y/%m/%d %H:%M')
    end_time = DateTimeField('end_time', format='%Y/%m/%d %H:%M')
    intro = TextAreaField('intro')

    def create_choices(self):
        ages = Age.query.all()
        self.age_id.choices = [(age.id, age.age) for age in ages]

    def create_activity(self):
        activity = Activity(organization_id=current_user.id,
                            name=self.name.data,
                            age_id=self.age_id.data,
                            price=int(self.price.data),
                            created=time.time(),
                            start_time=time.mktime(
                                self.start_time.data.timetuple()),
                            end_time=time.mktime(
                                self.end_time.data.timetuple()),
                            intro=self.intro.data)
        return activity


class CommentForm(Form):
    stars = IntegerField('stars')
    body = TextAreaField('body')

    def create_organization_comment(self, id):
        comment = OrganizationComment(organization_id=id,
                                  user_id=current_user.id,
                                  stars=self.stars.data,
                                  body=self.body.data,
                                  created=time.time())
        return comment
