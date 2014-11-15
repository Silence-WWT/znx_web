# -*- coding: utf-8 -*-
from . import course
from .forms import TimeForm, DetailForm, CommentForm, ConfirmForm
from ..models import Class, ClassOrder, ClassComment
from .. import db
from flask import render_template, redirect, \
    url_for, abort, current_app, request
from flask.ext.login import current_user


@course.route('/home/<int:id>', methods=['GET', 'POST'])
def home(id):
    course = Class.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment=form.create_class_comment(id)
        db.session.add(comment)
        db.session.commit()
        redirect(url_for('.home', id=id))
    page = request.args.get('page', 1, type=int)
    pagination = ClassComment.query.filter_by(class_id=id).order_by(
        ClassComment.created.asc()).paginate(
        page, per_page=current_app.config['ORG_COMMENT_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    course.page_view = course.page_view+1
    db.session.add(course)
    db.session.commit()
    org = course.get_org()
    return render_template('organclass_py.html', course=course, org=org,
                           comments=comments, form=form, pagination=pagination)


@course.route('/taste/<int:id>', methods=['GET', 'POST'])
def taste(id):
    course = Class.query.get_or_404(id)
    form = TimeForm()
    if form.validate_on_submit():
        order = form.create_ord(id)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('.detail', id=order.id))
    return render_template('classattend1_py.html', course=course, form=form)


@course.route('/detail/<int:id>', methods=['GET', 'POST'])
def detail(id):
    form = DetailForm()
    order = ClassOrder.query.get_or_404(id)
    if order.unified_id != current_user.get_unified_id():
        abort(404)
    if order.is_submitted:
        abort(404)
    if form.validate_on_submit():
        form.set_ord(order)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('.confirm', id=id))
    return render_template('classattend2_py.html', form=form)


@course.route('/confirm/<int:id>', methods=['GET', 'POST'])
def confirm(id):
    form = ConfirmForm()
    order = ClassOrder.query.get_or_404(id)
    course = Class.query.get_or_404(order.class_id)
    if order.unified_id != current_user.get_unified_id():
        abort(404)
    if order.is_submitted:
        abort(404)
    if form.validate_on_submit():
        order.remark = form.remark.data
        order.is_confirmed = True
        org = course.get_org()
        org.orders += 1
        db.session.add(order)
        db.session.add(org)
        db.session.commit()
        return redirect(url_for('course.success', id=order.id))
    return render_template('classattend3_py.html', form=form,
                           order=order, course=course)


@course.route('/success/<int:id>')
def success(id):
    order = ClassOrder.query.get_or_404(id)
    if order.unified_id != current_user.get_unified_id():
        abort(404)
    course = Class.query.get_or_404(order.class_id)
    org = course.get_org()
    return render_template('classattend4_py.html', org=org, order=order, course=course)
