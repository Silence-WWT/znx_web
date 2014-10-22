# -*- coding: utf-8 -*-
from . import org
from .. import db
from ..models import Organization, Type, Profession, Property, Size
from .forms import RegistrationForm, DetailForm
from flask.ext.login import login_user, login_required
from flask import redirect, url_for, render_template, flash, request


@org.route('/login', methods=['POST'])
def login():
    return render_template('auth/login.html')


@org.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        organization = Organization(cellphone=form.cellphone.data,
                            password=form.password.data)
        db.session.add(organization)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # TODO: Add token.
        # TODO: add macro in template for errors.
        #send_email(user.email, 'Confirm Your Account',
        #           'auth/mail/confirm', user=user)
        #flash('A confirmation email has been sent to you by email.')
        login_user(organization)
        return redirect(url_for('main.index'))
    return render_template('organ_regiter_py.html', form=form)


@org.route('/detail', methods=['GET', 'POST'])
@login_required
def detail():
    form = DetailForm()
    if form.validate_on_submit():
        organization = Organization(cellphone=form.cellphone.data,
                                    password=form.password.data)
        db.session.add(organization)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # TODO: Add token.
        # TODO: add macro in template for errors.
        #send_email(user.email, 'Confirm Your Account',
        #           'auth/mail/confirm', user=user)
        #flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    else:
        form.type_id.choices = [(t.id, t.type) for t in Type.query.all()]
        form.property_id.choices = [(t.id, t.property)
                                      for t in Property.query.all()]
        form.profession_id.choices = [(t.id, t.profession)
                                      for t in Profession.query.all()]
        form.size_id.choices = [(t.id, t.size)
                                      for t in Size.query.all()]
    return render_template('organ_regiter2_py.html', form=form)


@org.route('/certification', methods=['GET', 'POST'])
def certification():
    form = RegistrationForm()
    if form.validate_on_submit():
        organization = Organization(cellphone=form.cellphone.data,
                                    password=form.password.data)
        db.session.add(organization)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # TODO: Add token.
        # TODO: add macro in template for errors.
        #send_email(user.email, 'Confirm Your Account',
        #           'auth/mail/confirm', user=user)
        #flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('organ_regiter3_py.html', form=form)
