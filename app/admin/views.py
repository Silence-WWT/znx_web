# -*- coding: utf-8 -*-
from . import admin
from .. import db
from flask import render_template
from ..models import ChatLine, Organization, UnifiedId

@admin.route('/chat')
def chat():
    channels = db.session.query(ChatLine.unified_id, ChatLine.organization_id).\
        group_by(ChatLine.unified_id, ChatLine.organization_id).\
        order_by(ChatLine.id.desc())
    chat_groups = list()
    for channel in channels:
        chatlines=ChatLine.query.filter(
            ChatLine.unified_id==channel.unified_id,
            ChatLine.organization_id==channel.organization_id).all()
        org_name = db.session.query(Organization.name). \
            filter(Organization.id==channel.organization_id).first()
        mobile = UnifiedId.query.get(channel.unified_id).get_mobile()
        chat_groups.append((chatlines, org_name.name, mobile))
    return render_template('admin_talk.html', chat_groups=chat_groups)

