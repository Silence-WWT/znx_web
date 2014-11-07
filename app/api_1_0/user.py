# -*- coding: utf-8 -*-
import json
import time
from random import randint, seed
from urllib2 import urlopen
from xml.dom import minidom

from flask import request

from app import db
from ..models import User, UnifiedId, ChatLine
from . import api
from api_constants import *
from helper import get_unified


@api.route('/register')
def register():
    data = {}
    username = request.args.get('username', '').encode('utf8')
    password = request.args.get('password')
    mobile = request.args.get('mobile')
    identity = request.args.get('identity')
    email = request.args.get('email', '')
    if User.query.filter_by(username=username).first():
        data['status'] = USERNAME_EXIST
        return json.dumps(data)
    if username and password and mobile:
        user = User(
            username=username,
            password=password,
            mobile=mobile,
            identity=identity,
            email=email,
            is_email_confirmed=False,
            created=time.time()
        )
        db.session.add(user)
        db.session.commit()
        unified = get_unified(user.id, identity)
        data['user'] = {
            'user_id': user.id,
            'username': username,
            'mobile': mobile,
            'identity': identity,
            'email': email,
            'unified': unified.id,
            'chat_line': 0
        }
        data['status'] = SUCCESS
    else:
        data['status'] = PARAMETER_ERROR
    return json.dumps(data)


@api.route('/login')
def login():
    data = {}
    mobile = request.args.get('mobile', u'', type=unicode)
    password = request.args.get('password')
    identity = request.args.get('identity')
    user = User.query.filter_by(mobile=mobile).first()
    if not user:
        user = User.query.filter_by(username=mobile).first()
    if user is not None and user.verify_password(password):
        unified = UnifiedId.query.filter_by(user_id=user.id).first()
        chat_line = ChatLine.query.filter_by(unified_id=unified.id, is_user=False).order_by(-ChatLine.created).first()
        if chat_line:
            last_id = chat_line.id
        else:
            last_id = 0
        if user.identity != identity and identity:
            user.identity = identity
        data['status'] = SUCCESS
        data['user'] = {
            'user_id': user.id,
            'username': user.username,
            'mobile': user.mobile,
            'email': user.email,
            'identity': user.identity,
            'chat_line': last_id,
            'unified': unified.id,
        }
    else:
        data['status'] = LOGIN_FAILED
    return json.dumps(data)


seed()


@api.route('/mobile_confirm')
def mobile_confirm():
    data = {}
    mobile = request.args.get('mobile')
    if User.query.filter_by(mobile=mobile).first():
        data['status'] = MOBILE_EXIST
    elif mobile:
        verify_code = randint(100000, 999999)
        content = MESSAGE_API_CONTENT_TEST.format(verify_code=verify_code)
        message_url = MESSAGE_API_URL.format(account=MESSAGE_API_ACCOUNT, password=MESSAGE_API_PASSWORD,
                                             mobile=mobile, content=content)
        response = urlopen(message_url.encode('utf8')).read()
        doc = minidom.parseString(response)
        code = doc.getElementsByTagName('code')[0].firstChild.nodeValue
        if code != str(MESSAGE_API_SUCCESS):
            data['status'] = MESSAGE_CONFIRM_FAIL
        else:
            data['status'] = SUCCESS
            data['verify_code'] = verify_code
    else:
        data['status'] = PARAMETER_ERROR
    return json.dumps(data)
