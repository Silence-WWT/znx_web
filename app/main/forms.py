# -*- coding: utf-8 -*-
import time
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField, \
    TextAreaField, BooleanField, RadioField, DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from ..models import Register, SiteComment


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


class SiteCommentForm(Form):
    mobile = StringField()
    body = TextAreaField()

    def create_comment(self):
        comment = SiteComment(mobile=self.mobile.data,
                              body=self.body.data,
                              created=time.time())
        return comment
