# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import User
from . import api
from api_constants import *


@api.route('/login')
def login():
    data = {}
    cellphone = request.args.get('cellphone')
    password = request.args.get('password')
    identity = request.args.get('identity')
    user = User.query.filter_by(cellphone=cellphone).first()
    if user is not None and user.verify_password(password):
        if user.identity != identity and identity:
            user.identity = identity
        data[STATUS] = SUCCESS
        data['user'] = {
            'username': user.username,
            'cellphone': user.cellphone,
            'email': user.email,
            'identity': user.identity
        }
    else:
        data[STATUS] = LOGIN_FAILED
    return json.dumps(data)