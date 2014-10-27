# -*- coding: utf-8 -*-
import time
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField, \
    TextAreaField, BooleanField, RadioField, DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from ..models import Register


class RegisterForm(Form):
    city_id = SelectField(coerce=int)
    mobile = StringField()
    name = StringField()
    need =TextAreaField()

    def create_register(self):
        register = Register(city_id=self.city_id.data,
                            mobile=self.mobile.data,
                            name=self.name.data,
                            need=self.need.data,
                            created=time.time())
        return register
