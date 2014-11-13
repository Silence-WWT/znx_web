# -*- coding: utf-8 -*-
import time
from . import chat
from .. import db
from flask import request, jsonify
from flask.ext.login import current_user
from ..permission import user_permission
from ..models import ChatLine, UnifiedId


@chat.route('/chat', methods=['GET', 'POST'])
@user_permission.require()
def chat():
    channel_id = current_user.get_unified_id()
    if not UnifiedId.query.get_or_404(channel_id).user_id:
        return 'false', 404
    organization_id = request.values.get('orgid', 0, type=int)
    if request.method == 'GET':
        last_id = request.values.get('id', 1, type=int)
        if last_id:
            chatline = ChatLine.query.\
                filter(ChatLine.unified_id == channel_id).\
                filter(ChatLine.is_user == False).\
                filter(organization_id == organization_id).\
                filter(ChatLine.id > last_id).first()
            if chatline:
                return jsonify({'id': chatline.id,
                                'content': chatline.content})
            return 'false', 500
        else:
            return 'false', 500

    else:
        content = request.values.get('context', None, type=unicode)
        if content and organization_id:
            chat_line = ChatLine(unified_id=channel_id,
                                 is_user=True,
                                 content=content,
                                 created=time.time(),
                                 organization_id=organization_id,
                                 source=1)

            db.session.add(chat_line)
            try:
                db.session.commit()
                return jsonify({'id': chat_line.id})
            except:
                db.session.rollback()
                raise
        return 'false', 500
