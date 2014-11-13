# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField, IntegerField
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, Email, EqualTo
from ..models import Organization

class ReplyForm(Form):
    content = TextAreaField('content', validators=[DataRequired()])


class RecommendedOrgForm(Form):
    org_id = IntegerField('org_id')
    photo = FileField(validators=[
        FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    url = StringField('url', validators=[Length(0, 255)])

    def validate_org_id(self, field):
        if not Organization.query.filter_by(id=field.data).first():
            raise ValidationError(u'机构不存在')


class RecommendedActivityForm(Form):
    photo = FileField(validators=[
        FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    url = StringField('url', validators=[Length(0, 255)])
