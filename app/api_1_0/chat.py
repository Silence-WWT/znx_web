# -*- coding: utf-8 -*-
import json
import time

from flask import request

from app import db
from ..models import User, Organization, ChatLine, UnifiedId
from . import api
from api_constants import *


@api.route('/chat_get')
def chat_get():
    data = {'chat_lines': []}
    user_id = request.args.get('user_id')
    last_id = request.args.get('last_id')
    unified = UnifiedId.query.filter_by(user_id=user_id).first()
    if unified:
        chat_lines = ChatLine.query.\
            filter(ChatLine.unified_id == unified.id).\
            filter(ChatLine.is_user == False).\
            filter(ChatLine.id > last_id).\
            order_by(ChatLine.created)
        for chat_line in chat_lines:
            organization = Organization.query.get(chat_line.organization_id)
            data['chat_lines'].append({
                'chat_line': chat_line.id,
                'org_name': organization.name,
                'org_id': organization.id,
                'content': chat_line.content,
                'created': chat_line.created
            })
        data['status'] = SUCCESS
    else:
        data['status'] = PARAMETER_ERROR
    return json.dumps(data)


@api.route('/chat_post')
def chat_post():
    data = {}
    user_id = request.args.get('user_id')
    content = request.args.get('content', '').encode('utf8')
    unified_id = request.args.get('unified')
    org_id = request.args.get('org_id')
    organization = Organization.query.get(org_id)
    user = User.query.filter_by(id=user_id).first()
    if user and content and unified_id and organization:
        chat_line = ChatLine(
            unified_id=unified_id,
            is_user=True,
            content=content,
            source=CHAT_SOURCE_ANDROID,
            organization_id=organization.id,
            created=time.time()
        )
        db.session.add(chat_line)
        db.session.commit()
        data['status'] = SUCCESS
    else:
        data['status'] = PARAMETER_ERROR
    return json.dumps(data)