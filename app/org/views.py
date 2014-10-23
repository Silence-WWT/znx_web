# -*- coding: utf-8 -*-
import os
from uuid import uuid4
from . import org
from .. import db
from ..models import Organization, Type, Profession, Property, Size, Location
from .forms import RegistrationForm, DetailForm, CertificationForm, LoginForm
from ..user.forms import  LoginForm as UserLoginForm
from flask.ext.login import login_user, login_required, current_user
from flask import redirect, url_for, render_template,\
    flash, current_app, request


@org.route('/login', methods=['POST'])
def login():
    user_form = UserLoginForm()
    org_form = LoginForm()
    if org_form.validate_on_submit():
        org = Organization.query.filter_by(cellphone=org_form.cellphone.data).first()
        if org is not None and org.verify_password(user_form.password.data):
            login_user(org, user_form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户名密码错误')
    return render_template('login_choose_py.html',
                           user_form=user_form,
                           org_form=org_form)


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
def detail():
    form = DetailForm()
    form.type_id.choices = [(t.id, t.type) for t in Type.query.all()]
    form.property_id.choices = [(t.id, t.property)
                                for t in Property.query.all()]
    form.profession_id.choices = [(t.id, t.profession)
                                  for t in Profession.query.all()]
    form.size_id.choices = [(t.id, t.size)
                            for t in Size.query.all()]
    form.location_id.choices = [(t.id, t.district)
                                for t in Location.query.all()]
    locations = Location.query.all()
    location_dict = dict()
    for location in locations:
        if location.city not in location_dict.keys():
            location_dict[location.city] = set()
        location_dict[location.city].add((location.id,
                                          location.district))
    form.location = location_dict
    if form.validate_on_submit():
        current_user.type = form.type_id.data
        current_user.name = form.name.data
        current_user.profession = form.profession_id.data
        current_user.property_ = form.property_id.data
        current_user.size = form.size_id.data
        current_user.contact = form.contact.data
        current_user.location = form.location_id.data
        current_user.address = form.address.data
        current_user.intro = form.intro.data
        db.session.add(current_user)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # TODO: Add token.
        # TODO: add macro in template for errors.
        #send_email(user.email, 'Confirm Your Account',
        #           'auth/mail/confirm', user=user)
        #flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('organ_regiter2_py.html', form=form)


@org.route('/certification', methods=['GET', 'POST'])
def certification():
    form = CertificationForm()
    if form.validate_on_submit():
        #organization = Organization(cellphone=form.cellphone.data,
        # #password=form.password.data)
        #db.session.add(organization)
        #db.session.commit()
        # token = user.generate_confirmation_token()
        # TODO: Add token.
        # TODO: add macro in template for errors.
        #send_email(user.email, 'Confirm Your Account',
        #           'auth/mail/confirm', user=user)
        #flash('A confirmation email has been sent to you by email.')
        path = current_app.config['PHOTO_DIR']

        certification = uuid4().hex
        ext = form.certification.data.filename.rsplit('.', 1)[-1]
        file_path = os.path.join(path, certification+'.'+ext)
        form.certification.data.save(file_path)

        photo = uuid4().hex
        ext = form.photo.data.filename.rsplit('.', 1)[-1]
        file_path = os.path.join(path, photo+'.'+ext)
        form.photo.data.save(file_path)
        current_user.authorization = certification
        current_user.photo = photo
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('organ_regiter3_py.html', form=form)
