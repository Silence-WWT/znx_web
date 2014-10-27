# -*- coding: utf-8 -*-
from . import course
from .forms import TimeForm, DetailForm, CommentForm
from ..models import Class, ClassOrder
from .. import db
from flask import render_template, redirect, url_for, abort
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
    return render_template('organclass_py.html', course=course, form=form)


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
    if order.user_id != current_user.id:
        abort(404)
    if form.validate_on_submit():
        form.set_ord(order)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('classattend2_py.html', form=form)


