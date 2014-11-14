# -*- coding: utf-8 -*-
import time
from . import admin
from .. import db
from flask import render_template, request, current_app, redirect, url_for, flash
from ..models import ChatLine, Organization, UnifiedId,\
    Register, RecommendedActivity, RecommendedOrg, SiteComment
from .form import ReplyForm, RecommendedActivityForm, RecommendedOrgForm, OrgForm
from ..utils.captcha import send_confirm_sms

@admin.route('/chat', methods=['GET', 'POST'])
def chat():
    replyform = ReplyForm()
    if replyform.validate_on_submit():
        orgid = request.values.get('orgid', 0, type=int)
        unified_id = request.values.get('unified_id', 0, type=int)
        if orgid and unified_id:
            chat= ChatLine(unified_id=unified_id,
                           is_user=False,
                           content=replyform.content.data,
                           source=1,
                           organization_id=orgid,
                           created=time.time())
            db.session.add(chat)
            db.session.commit()
    channels = db.session.query(ChatLine.unified_id, ChatLine.organization_id).\
        group_by(ChatLine.unified_id, ChatLine.organization_id).\
        order_by(ChatLine.id.desc())
    chat_groups = list()
    for channel in channels:
        session = dict()
        session['chatlines']=ChatLine.query.filter(
            ChatLine.unified_id==channel.unified_id,
            ChatLine.organization_id==channel.organization_id).all()
        session['org'] = Organization.query.get(channel.organization_id)
        session['mobile'] = UnifiedId.query.get(channel.unified_id).get_mobile()
        session['channel'] = channel
        chat_groups.append(session)

    return render_template('admin_talk.html', chat_groups=chat_groups, form=replyform)


@admin.route('/register', methods=['GET'])
def register():
    page = request.args.get('page', 1, type=int)
    pagination = Register.query.order_by(
        Register.created.desc()).paginate(
        page, per_page=current_app.config['ADMIN_REGISTER_PER_PAGE'],
        error_out=False)
    registers = pagination.items
    return render_template('admin_asklearn.html',
                           registers=registers,
                           pagination=pagination)


@admin.route('/comment', methods=['GET'])
def comment():
    page = request.args.get('page', 1, type=int)
    pagination = SiteComment.query.order_by(
        Register.created.desc()).paginate(
        page, per_page=current_app.config['ADMIN_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('admin_asklearn.html',
                           comments=comments,
                           pagination=pagination)


@admin.route('/add_org', methods=['GET', 'POST'])
def search_org():
    form = OrgForm()
    if form.validate_on_submit():
        return redirect(url_for('.add_org', org_id=form.org_id.data))
    return render_template('admin_indexoriganadd1.html', form=form)


@admin.route('/add_org/<int:org_id>', methods=['GET', 'POST'])
def add_org(org_id):
    Organization.query.get_or_404(org_id)
    form = RecommendedOrgForm()
    form.org_id.data = org_id
    form.url.data = url_for('org.home', id=org_id)
    if form.validate_on_submit():
       org = RecommendedOrg(org_id=form.org_id.data,
                            photo=form.photo.data,)
        # TODO: complete.
    return render_template('admin_indexoriganadd2.html')

@admin.route('/org', methods=['GET'])
def org():
    return render_template('admin_indexorigan.html')


@admin.route('/activity', methods=['GET'])
def activity():
    return render_template('admin_indexactivity.html')


@admin.route('/confirm_list', methods=['GET'])
def confirm_list():
    page = request.args.get('page', 1, type=int)
    pagination = Organization.query.filter_by(source_site_id=0).\
        order_by(Organization.id.desc()).paginate(
        page, per_page=current_app.config['ADMIN_ORG_PER_PAGE'], error_out=False)
    orgs = pagination.items
    return render_template('admin_origanlist.html',
                           orgs=orgs,
                           pagination=pagination)


@admin.route('/confirm/<int:org_id>')
def confirm(org_id):
    org = Organization.query.get_or_404(org_id)
    return render_template('admin_origancome.html', org=org)


@admin.route('/set_confirm/<int:org_id>')
def set_confirm(org_id):
    org = Organization.query.get_or_404(org_id)
    if org.is_confirmed == False:
        org.is_confirmed = True
        db.session.add(org)
        db.session.commit()
        if send_confirm_sms(str(org.mobile)):
            flash(u'设置成功')
        else:
            flash(u'发送失败')

    else:
        org.is_confirmed = False
        db.session.add(org)
        db.session.commit()
    return redirect(url_for('znx_admin.confirm', org_id=org_id))
