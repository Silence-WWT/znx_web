# -*- coding: utf-8 -*-
import uuid
import time
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField,\
    SelectMultipleField, TextAreaField, BooleanField, RadioField, \
    DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import ValidationError
from .. import db
from ..models import Organization, Age, Class, Activity, OrganizationComment,\
    Time, Type, Profession, Location, City, OrganizationAge,\
    OrganizationProfession
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
    slogan = StringField('slogan', validators=[DataRequired(u'必填'),
                                               Length(1, 30, u'广告语长度不符合规范')])
    contact = StringField('contact',
                          validators=[DataRequired(u'必填'),
                                      Length(1, 6, u'联系人长度不符合规范')])
    contact_phone = StringField(
        'contact_phone',
        validators=[Length(0, 255, u'联系电话长度不符合要求')])
    address = StringField('address',
                          validators=[DataRequired(u'必填'),
                                      Length(1, 40, u'地址长度不符合规范')])
    traffic = StringField('traffic', validators=[Length(0, 200, u'附近交通不符合要求')])
    detail = TextAreaField('detail',
                          validators=[DataRequired(u'必填'),
                                      Length(1, 140, u'简介长度不符合规范')])
    site = StringField('site', validators=[Length(0, 255, u'网址长度太长')])

    location_id = SelectField(coerce=int)
    professions = SelectMultipleField('org_profession',
                                     validators=[DataRequired(u'至少选一项')],
                                     coerce=int,
                                     widget=select_multi_checkbox)

    ages = SelectMultipleField('org_ages',
                                      validators=[DataRequired(u'至少选一项')],
                                      coerce=int,
                                      widget=select_multi_checkbox)

    def create_choices(self):

        self.type_id.choices = [(t.id, t.type) for t in Type.query.all()]
        self.professions.choices = [(t.id, t.profession)
                                    for t in Profession.query.all()]
        self.location_id.choices = [(t.id, t.district)
                                    for t in Location.query.all()]
        self.ages.choices = [(t.id, t.age)
                                    for t in Age.query.all()]
        self.city_id = City.query.all()
        self.location = Location.query.all()

    def update_org(self):
        current_user.type_id = self.type_id.data
        current_user.name = self.name.data
        current_user.slogan = self.slogan.data
        current_user.contact = self.contact.data
        current_user.contract_phone = self.contact_phone.data
        current_user.address = self.address.data
        current_user.traffic = self.traffic.data
        current_user.detail = self.detail.data
        current_user.site = self.site.data
        current_user.location_id = self.location_id.data
        db.session.add(current_user)
        db.session.commit()

        # profession
        org_professions = OrganizationProfession.query.\
            filter_by(organization_id=current_user.id).all()
        for org_profession in org_professions:
            db.session.delete(org_profession)
        for profession_id in self.professions.data:
            org_profession = OrganizationProfession(
                organization_id=current_user.id,
                profession_id=profession_id)
            db.session.add(org_profession)

        db.session.commit()

        # ages
        org_ages = OrganizationAge.query. \
            filter_by(organization_id=current_user.id).all()
        for org_age in org_ages:
            db.session.delete(org_age)
        for age_id in self.ages.data:
            org_age = OrganizationAge(
                organization_id=current_user.id,
                age_id=age_id)
            db.session.add(org_age)
        db.session.commit()


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
    price = IntegerField('price')
    consult_time = StringField('consult_time', validators=[
                               DataRequired(u'必填'),
                               Length(1, 20, u'长度不超过20字符')])
    days = IntegerField('days')
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

    def init_from_class(self, class_id):
        course = Class.query.get_or_404(class_id)
        self.name.data = course.name
        self.age_id.data = course.age_id
        self.price.data = course.price
        self.consult_time.data = course.consult_time
        self.is_tastable.data = int(course.is_tastable)
        self.is_round.data = int(course.is_round)
        self.days.data = course.days
        self.intro.data = course.intro

    def update_course(self, class_id):
        course = Class.query.get_or_404(class_id)
        course.name = self.name.data
        course.age_id = self.age_id.data
        course.price = self.price.data
        course.consult_time = self.consult_time.data
        course.is_tastable = bool(self.is_tastable.data)
        course.is_round = bool(self.is_round.data)
        course.days = self.days.data
        course.intro = self.intro.data
        return course


class ActivityForm(Form):
    name = StringField('name', validators=[DataRequired(u'必填'),
                                           Length(1, 30, u'30字符以内')])
    age_id = SelectField('age_id', coerce=int)
    price = IntegerField('prince')
    start_time = DateTimeField('start_time', format='%Y/%m/%d %H:%M')
    end_time = DateTimeField('end_time', format='%Y/%m/%d %H:%M')
    intro = TextAreaField('intro', validators=[DataRequired(u'必填'),
                                               Length(1, 140,u'140字符以内')])

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

    def init_from_activity(self, activity_id):
        activity = Activity.query.get_or_404(activity_id)
        self.name.data = activity.name
        self.age_id.data = activity.age_id
        self.price.data = activity.price
        self.start_time.data = datetime.fromtimestamp(activity.start_time)
        self.end_time.data = datetime.fromtimestamp(activity.end_time)
        self.intro.data = activity.intro

    def update_activity(self, activity_id):
        activity = Activity.query.get_or_404(activity_id)
        activity.name = self.name.data
        activity.age_id = self.age_id.data
        activity.price = self.price.data
        activity.start_time = time.mktime(
            self.start_time.data.timetuple())
        activity.end_time = time.mktime(
            self.end_time.data.timetuple())
        activity.intro = self.intro.data
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
