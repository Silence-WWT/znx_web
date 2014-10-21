# -*- coding: utf-8 -*-
from . import test
from ..models import User, Organization
from flask import redirect, url_for
from flask.ext.login import login_user


@test.route('/user/<id>')
def user_login(id):
    user = User.query.filter_by(id=id)
    login_user(user)
    return redirect(url_for('main.index'))

@test.route('/org/<id>')
def org_login(id):
    org = Organization.query.filter_by(id=id)
    login_user(org)
    return redirect(url_for('main.index'))


