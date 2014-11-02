# -*- coding: utf-8 -*-
import time
from . import chat
from .. import db
from flask import request, jsonify
from flask.ext.login import current_user
from ..models import UnifiedId, ChatLine



@chat.route('/chat', methods=['GET', 'POST'])
def chat():
    channel_id = current_user.get_unified_id()
    if request.method == 'GET':
        last_id = request.valuse.get('id', 1, type=int)
        if last_id:
            chatline = ChatLine.query.filte(ChatLine.unified_id==channel_id).\
                filter(ChatLine.is_user==False).\
                filter(ChatLine.id>last_id).first()
            return jsonify({'id': chatline.id,
                            'content':chatline.content})
        else:
            return 'false', 500

    else:
        content = request.values.get('context', None, type=unicode)
        if content:
            chat_line = ChatLine(unified_id=channel_id,
                      is_user=True,
                      content=content,
                      created=time.time())
            db.session.add(chat_line)
            try:
                db.session.commit()
                return 'ok'
            except :
                db.session.rollback()
                raise
