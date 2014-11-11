# -*- coding: utf-8 -*-
from flask import Blueprint
from .. import admin as admin_app
from ..models import User, Organization, Class, Activity, Time, Age, Type
from .. import db
from flask.ext.admin.contrib.sqla import ModelView

admin = Blueprint('znx_admin', __name__)
from . import views
admin_app.add_view(ModelView(User, db.session))
admin_app.add_view(ModelView(Organization, db.session))
admin_app.add_view(ModelView(Class, db.session))
admin_app.add_view(ModelView(Activity, db.session))
admin_app.add_view(ModelView(Time, db.session))
admin_app.add_view(ModelView(Age, db.session))
admin_app.add_view(ModelView(Type, db.session))

