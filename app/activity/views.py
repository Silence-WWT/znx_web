# -*- coding: utf-8 -*-
from . import activity
from .. import db
from .forms import DetailForm, ConfirmForm, CommentForm
from ..models import Activity, ActivityOrder, ActivityComment
from flask import render_template, redirect, url_for, abort, request, \
    current_app
from flask.ext.login import current_user


@activity.route('/home/<int:id>', methods=['GET', 'POST'])
def home(id):
    activity = Activity.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = form.create_activity_comment(id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.home', id=id))
    page = request.args.get('page', 1, type=int)
    pagination = ActivityComment.query.filter_by(activity_id=id).order_by(
        ActivityComment.created.asc()).paginate(
        page, per_page=current_app.config['ORG_COMMENT_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    activity.page_view = activity.page_view+1
    db.session.add(activity)
    db.session.commit()
    return render_template('organact_py.html', activity=activity,
                           comments=comments, form=form, pagination=pagination)


@activity.route('/taste/<int:id>', methods=['GET', 'POST'])
def taste(id):
    Activity.query.get_or_404(id)
    form = DetailForm()
    if form.validate_on_submit():
        order = form.create_ord(id)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('.confirm', id=order.id))
    return render_template('activityattend1_py.html', form=form)


@activity.route('/confirm/<int:id>', methods=['GET', 'POST'])
def confirm(id):
    order = ActivityOrder.query.get_or_404(id)
    form = ConfirmForm()
    activity = Activity.query.get_or_404(order.activity_id)
    if order.user_id != current_user.id:
        abort(404)
    if form.validate_on_submit():
        order.remark = form.remark.data
        order.is_confirmed = True
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('activityattend2_py.html', activity=activity,
                           order=order, form=form)
