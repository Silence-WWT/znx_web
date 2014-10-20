# -*- coding: utf-8 -*-
from . import user
from .. import db
from .forms import LoginForm, RegistrationForm
from ..models import User
from ..email import send_email
from flask.ext.login import login_user
from flask import redirect, url_for, render_template, flash, request


@user.route('/login', methods=['POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # TODO: Add token.
        send_email(user.email, 'Confirm Your Account',
                   'auth/mail/confirm', user=user)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)