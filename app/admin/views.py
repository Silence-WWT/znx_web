# -*- coding: utf-8 -*-
import time
from . import admin
from .. import db
from flask import render_template, request
from ..models import ChatLine, Organization, UnifiedId
from .form import ReplyForm

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
    return render_template('admin_asklearn.html')


@admin.route('/org', methods=['GET'])
def org():
    return render_template('admin_indexorigan.html')


@admin.route('/activity', methods=['GET'])
def activity():
    return render_template('admin_indexactivity.html')


@admin.route('/admin', methods=['GET'])
def admin():
    return render_template('admin_origancome.html')
