# -*- coding: utf-8 -*-
import time
from flask.ext.wtf import Form
from flask.ext.login import current_user
from wtforms import DateTimeField, StringField, SelectField
from ..models import ClassOrder

class TimeForm(Form):
    time = DateTimeField('time', format='%Y/%m/%d %H:%M')
    campus = StringField('campus')

    def create_ord(self, id):
        class_order = ClassOrder(user_id=current_user.id,
                                 class_id=id,
                                 created=time.time(),
                                 time=time.mktime(self.time.data.timetuple()),
                                 name=u'',
                                 age=u'',
                                 sex=True,
                                 mobile='',
                                 email='',
                                 address=u'',
                                 campus=self.campus.data,
                                 remark=u'')
        return class_order


class DetailForm(Form):
    name = StringField('name')
    age = StringField('age')
    sex = SelectField('sex', choices=[(1, 'male'), (0, 'female')], coerce=int)
    cellphone = StringField('cellphone')
    address = StringField('address')

    def set_ord(self, order):
        order.name = self.name.data
        order.age = self.age.data
        order.sex = bool(self.sex.data)
        order.mobile = self.cellphone.data
        order.address = self.address.data
        return order


