# -*- coding: utf-8 -*-
import time
from flask.ext.wtf import Form
from flask.ext.login import current_user
from wtforms import DateTimeField, StringField,\
    SelectField, TextAreaField, IntegerField
from ..models import ActivityOrder, ActivityComment


class DetailForm(Form):
    name = StringField('name')
    age = StringField('age')
    sex = SelectField('sex', choices=[(1, 'male'), (0, 'female')], coerce=int)
    cellphone = StringField('cellphone')
    address = StringField('address')

    def create_ord(self, id):
        activity_order = ActivityOrder(unified_id=current_user.get_unified_id(),
                                       activity_id=id,
                                       created=time.time(),
                                       name=self.name.data,
                                       age=self.age.data,
                                       sex=bool(self.sex.data),
                                       email='',
                                       mobile=self.cellphone.data,
                                       address=self.address.data,
                                       remark=u'')
        return activity_order

    def set_from_order(self, order):
        self.name.data = order.name
        self.sex.data = order.sex
        self.cellphone.data = order.mobile
        self.address.data = order.address


class ConfirmForm(Form):
    remark = TextAreaField()


class CommentForm(Form):
    stars = IntegerField('stars')
    body = TextAreaField('body')

    def create_activity_comment(self, id):
        comment = ActivityComment(activity_id=id,
                                  user_id=current_user.id,
                                  stars=self.stars.data,
                                  body=self.body.data,
                                  created=time.time())
        return comment
