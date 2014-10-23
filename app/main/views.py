# -*- coding: utf-8 -*-
from . import main
from flask.ext.login import login_required, logout_user
from flask import redirect, url_for, render_template, flash
from ..user.forms import LoginForm as UserLoginForm
from ..org.forms import LoginForm as OrgLoginForm


@main.route('/login', methods=['GET'])
def login():
    user_form = UserLoginForm()
    org_form = OrgLoginForm()
    return render_template('login_choose_py.html',
                           user_form=user_form,
                           org_form=org_form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@main.route('/register')
def register():
    return render_template('reg_choose_py.html')

@main.route('/')
def index():
    return render_template('index_py.html')
