# -*- coding: utf-8 -*-
import os
from uuid import uuid4
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField, IntegerField
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, Email, EqualTo
from ..models import Organization
from flask import current_app
from ..utils.validator import generate_dir_path

class ReplyForm(Form):
    content = TextAreaField('content', validators=[DataRequired()])


class OrgForm(Form):
    org_id = IntegerField('org_id')
    def validate_org_id(self, field):
        if not Organization.query.filter_by(id=field.data).first():
            raise ValidationError(u'机构不存在')

class RecommendedOrgForm(Form):
    org_id = IntegerField('org_id')
    photo = FileField(validators=[
        FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    url = StringField('url', validators=[Length(0, 255)])

    def validate_org_id(self, field):
        if not Organization.query.filter_by(id=field.data).first():
            raise ValidationError(u'机构不存在')

    def save_pic(self):
        path = current_app.config['PHOTO_DIR']
        org_id = self.org_id.data
        relative_path = generate_dir_path(org_id)
        dir_path = os.path.join(path, relative_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        ext = self.photo.data.filename.rsplit('.', 1)[-1]
        photo = uuid4().hex + '.' + ext
        file_path = os.path.join(dir_path, photo)
        self.photo.data.save(file_path)

        return os.path.join(relative_path, photo)

class RecommendedActivityForm(Form):
    photo = FileField(validators=[
        FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    url = StringField('url', validators=[Length(0, 255)])
