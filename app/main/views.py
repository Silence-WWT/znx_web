# -*- coding: utf-8 -*-
from . import main
from .. import db
from .forms import RegisterForm
from flask.ext.login import login_required, logout_user
from flask import redirect, url_for, render_template, flash
from ..user.forms import LoginForm as UserLoginForm
from ..org.forms import LoginForm as OrgLoginForm
from ..models import City, Register


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
    registers = Register.query.order_by(Register.id.desc()).limit(6).all()
    return render_template('index_py.html', registers=registers)


@main.route('/learn', methods=['GET', 'POST'])
def learn():
    form = RegisterForm()
    form.city_id.choices = [(t.id, t.city)
                            for t in City.query.all()]
    if form.validate_on_submit():
        register = form.create_register()
        db.session.add(register)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('asklearn_py.html', form=form)


@main.route('/download')
def download():
    return render_template('appdown_py.html')


@main.route('/workflow')
def workflow():
    return render_template('origanlead_py.html')
