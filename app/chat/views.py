# -*- coding: utf-8 -*-
from . import chat
from flask.ext.login import current_user
from ..models import UnifiedId


@chat.route('/chat', methods=['POST'])
def chat():
    channel_id = current_user.get_unified_id()
    return
