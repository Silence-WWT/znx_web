# -*- coding: utf-8 -*-
import uuid
import time
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField,\
    TextAreaField, BooleanField, RadioField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import ValidationError
from ..models import Organization, Age, Class, Activity, OrganizationComment
from flask.ext.login import current_user
from ..utils.validator import Captcha


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


class CourseForm(Form):
    name = StringField('name')
    age_id = SelectField('age_id', coerce=int)
    price = StringField('price')
    consult_time = StringField('consult_time')
    days = StringField('days')
    # TODO: days int
    is_tastable = RadioField('is_tastable', choices=[(1, 'yes'), (0, 'no')],
                             coerce=int)
    is_round = RadioField('is_round', choices=[(1, 'yes'), (0, 'no')],
                          coerce=int)
    intro = TextAreaField('intro')
    # TODO: add class time.

    def create_choices(self):
        ages = Age.query.all()
        self.age_id.choices = [(age.id, age.age) for age in ages]

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
                       days=int(self.days.data),
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
