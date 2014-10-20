# -*- coding: utf-8 -*-
from . import org
from ..models import User
from flask.ext.login import login_user
from flask import redirect, url_for, render_template, flash, request


@org.route('login', methods=['POST'])
def org_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)
