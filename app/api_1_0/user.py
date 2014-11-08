# -*- coding: utf-8 -*-
import json
import time
import redis
from random import randint
from urllib2 import urlopen
from xml.dom import minidom

from flask import request

from app import db
from app.models import User, UnifiedId, ChatLine
from app.utils.captcha import send_captcha
from . import api
from api_constants import *
from utils import get_unified


@api.route('/register')
def register():
    data = {}
    local_redis = redis.StrictRedis(host='localhost', port=6379, db=0)
    username = request.values.get('username', u'', type=unicode)
    password = request.values.get('password', '', type=str)
    mobile = request.values.get('mobile', '', type=str)
    identity = request.values.get('identity', '', type=str)
    email = request.values.get('email', '', type=str)
    verify_code = request.values.get('verify_code', '', type=str)

    key = 'captcha:user:' + mobile
    captcha = local_redis.get(key)
    if captcha != verify_code:
        data['status'] = VERIFY_CODE_INCORRECT
    elif User.query.filter_by(username=username).first():
        data['status'] = USERNAME_EXIST
    elif username and password and mobile:
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


@api.route('/mobile_confirm')
def mobile_confirm():
    data = {}
    mobile = request.values.get('mobile', '', type=str)
    if User.query.filter_by(mobile=mobile).first():
        data['status'] = MOBILE_EXIST
    elif mobile:
        status = send_captcha('user', mobile)
        if status:
            data['status'] = SUCCESS
        else:
            data['status'] = MESSAGE_CONFIRM_FAIL
    else:
        data['status'] = PARAMETER_ERROR
    return json.dumps(data)


@api.route('/reset_password')
def reset_password():
    data = {}
    local_redis = redis.StrictRedis(host='localhost', port=6379, db=0)
    password = request.values.get('password', '', type=str)
    mobile = request.values.get('mobile', '', type=str)
    verify_code = request.values.get('verify_code', '', type=str)

    key = 'captcha:user:' + mobile
    captcha = local_redis.get(key)
    user = User.query.filter_by(mobile=mobile).first()
    if captcha != verify_code:
        data['status'] = VERIFY_CODE_INCORRECT
    elif user:
        user.password = password
        data['status'] = SUCCESS
    else:
        data['status'] = USER_NOT_EXIST
    return json.dumps(data)