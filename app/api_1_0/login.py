# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import User
from . import api
from api_constants import *


@api.route('/login')
def login():
    data = {}
    mobile = request.args.get('mobile')
    password = request.args.get('password')
    identity = request.args.get('identity')
    user = User.query.filter_by(mobile=mobile).first()
    if user is not None and user.verify_password(password):
        if user.identity != identity and identity:
            user.identity = identity
        data['status'] = SUCCESS
        data['user'] = {
            'username': user.username,
            'mobile': user.mobile,
            'email': user.email,
            'identity': user.identity
        }
    else:
        data['status'] = LOGIN_FAILED
    return json.dumps(data)