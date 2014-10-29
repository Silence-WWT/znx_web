# -*- coding: utf-8 -*-
import time
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField, \
    TextAreaField, BooleanField, RadioField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from ..models import Register, SiteComment, Type, Profession, Property, Size,\
    Location


class RegisterForm(Form):
    city_id = SelectField(coerce=int)
    mobile = StringField()
    name = StringField()
    need = TextAreaField()

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


class SearchForm(Form):
    name = StringField('name')
    type_id = SelectField('type', coerce=int)
    profession_id = SelectField('profession', coerce=int)
    property_id = SelectField('property', coerce=int)
    size_id = SelectField('size', coerce=int)
    location_id = SelectField('location', coerce=int)
    is_confirmed = RadioField('is_confirmed',
                              choices=[(1, 'yes'), (0, 'no'), (-1, 'all')],
                              coerce=int)
    submit = SubmitField('submit')

    def create_choices(self, city_id):

        all = [(0, u'全部')]

        types = [(type.id, type.type) for type in Type.query.all() ]
        types.extend(all)
        self.type_id.choices = types

        professions = [(profession.id, profession.profession)
                       for profession in Profession.query.all()]
        professions.extend(all)
        self.profession_id.choices = professions

        properties = [(property.id, property.property)
                      for property in Property.query.all()]
        properties.extend(all)
        self.property_id.choices = properties

        sizes = [(size.id, size.size) for size in Size.query.all()]
        sizes.extend(all)
        self.size_id.choices = sizes

        locations = [(location.id, location.district)
                     for location in Location.query.filter(city_id == city_id).all()]
        locations.extend(all)
        self.location_id.choices = locations
