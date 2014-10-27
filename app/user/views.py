# -*- coding: utf-8 -*-
import time
from random import randint
from . import user
from .. import db
from .forms import LoginForm, RegistrationForm
from ..models import User, ActivityOrder, ClassOrder
from ..email import send_email
from ..org.forms import LoginForm as OrgLoginForm
from flask.ext.login import login_user, current_user
from flask import redirect, url_for, render_template, flash, request, jsonify
from ..utils.captcha import send_captcha


@user.route('/login', methods=['POST'])
def login():
    # TODO: add cellphone support.
    user_form = LoginForm()
    org_form = OrgLoginForm()
    if user_form.validate_on_submit():
        user = User.query.filter_by(username=user_form.username.data).first()\
        or User.query.filter_by(mobile=user_form.username.data).first()
        if user is not None and user.verify_password(user_form.password.data):
            login_user(user, user_form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户名密码错误')
    return render_template('login_choose_py.html',
                           user_form=user_form,
                           org_form=org_form)


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # TODO: add username
        user = User(email=form.email.data,
                    username=form.username.data,
                    mobile=form.cellphone.data,
                    password=form.password.data,
                    identity='',
                    created=time.time())
        db.session.add(user)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # TODO: Add token.
        #send_email(user.email, 'Confirm Your Account',
        #           'auth/mail/confirm', user=user)
        #flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('user_regiter_py.html', form=form)

@user.route('/send_sms', methods=['post'])
def send_sms():
    # TODO: add csrf and mobile check.
    # TODO: return 200 401
    mobile = request.values.get('mobile', '', type=str)
    #if mobile:
    #    send_captcha('user', mobile)
    return 'ok', 200


@user.route('/home')
def home():
    activity_orders = ActivityOrder.query.filter_by(user_id=current_user.id).\
        order_by(ActivityOrder.created.desc()).all()
    class_orders = ClassOrder.query.filter_by(user_id=current_user.id)
    # TODO: add class order, activity order. delete order.

    return render_template('userorderlist_py.html',
                           activity_orders=activity_orders,
                           class_orders=class_orders)

