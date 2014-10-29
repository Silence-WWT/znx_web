# -*- coding: utf-8 -*-
from . import test
from ..models import User, Organization
from flask import redirect, url_for, current_app
from flask.ext.login import login_user
from flask.ext.principal import Identity, identity_changed


@test.route('/user/<int:id>')
def user_login(id):
    user = User.query.filter_by(id=id).first()
    login_user(user)
    identity_changed.send(current_app._get_current_object(),
                          identity=Identity(user.get_id()))
    return redirect(url_for('main.index'))

@test.route('/org/<int:id>')
def org_login(id):
    org = Organization.query.filter_by(id=id).first()
    login_user(org)
    identity_changed.send(current_app._get_current_object(),
                          identity=Identity(org.get_id()))
    return redirect(url_for('main.index'))


