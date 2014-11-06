# -*- coding: utf-8 -*-
from . import main
from .. import db
from .forms import RegisterForm, SiteCommentForm, SearchForm
from flask.ext.login import login_required, logout_user
from flask.ext.principal import identity_changed, AnonymousIdentity
from flask import redirect, url_for, \
    render_template, flash, session, current_app, request
from ..user.forms import LoginForm as UserLoginForm
from ..org.forms import LoginForm as OrgLoginForm
from ..models import City, Register, Organization, Location, Profession


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
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    flash(u'您已经登出')
    return redirect(url_for('main.index'))


@main.route('/register')
def register():
    return render_template('reg_choose_py.html')


@main.route('/')
def index():
    registers = Register.query.order_by(Register.id.desc()).limit(5).all()
    city = City.query.first()
    if 'city_id' not in session:
        session['city_id'] = city.id
    city_id = int(session['city_id'])
    orgs = Organization.query.filter(
        Organization.location_id.in_(
            db.session.query(Location.id).filter(Location.city_id==city_id))).limit(3).all()
    return render_template('index_py.html', registers=registers, orgs=orgs)


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


@main.route('/join')
def join():
    return render_template('platformlead_py.html')


@main.route('/workflow')
def workflow():
    return render_template('origanlead_py.html')


@main.route('/about_us')
def about_us():
    return render_template('aboutus_py.html')


@main.route('/report', methods=['GET', 'POST'])
def report():
    form = SiteCommentForm()
    if form.validate_on_submit():
        comment = form.create_comment()
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('guestbook_py.html', form=form)


@main.route('/search', methods=['GET', 'POST'])
def search():
    professions = Profession.query.all()
    name = request.values.get('name', u'', type=unicode)
    profession_id = request.values.get('profession_id', 0, type=int)
    location_id  = request.values.get('location_id', 0, type=int)
    city_id  = request.values.get('city_id', 2, type=int)
    location_ids = db.session.query(Location.id).filter(Location.city_id==city_id)
    locations = Location.query.filter_by(city_id=city_id).all()

    query = Organization.query
    if profession_id:
        query=query.filter(Organization.profession_id==profession_id)
    if location_id:
        query=query.filter(Organization.location_id==location_id)
    else:
        query=query.filter(Organization.location_id.in_(location_ids))
    orgs = query.filter(Organization.name.like(u'%'+name+u'%')).all()
    return render_template('origanselect_py.html',
                           name=name,
                           location_id = location_id,
                           profession_id=profession_id,
                           orgs=orgs,
                           locations=locations,
                           professions=professions)


@main.route('/admin_talk', methods=['GET', 'POST'])
def admin_talk():
    return render_template('admin_talk.html')