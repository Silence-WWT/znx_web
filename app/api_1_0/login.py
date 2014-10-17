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
    user = User.query.filter_by(cellphone=cellphone).first()
    if user is not None and user.verify_password(password):
        # user.update_uuid(request.args.get('uuid'))
        # 待数据库表建完整后再适当修改
        # TODO: update uuid.
        data[STATUS] = SUCCESS
        data['username'] = user.username
        data['cellphone'] = user.cellphone
        data['email'] = user.email
        data['uuid'] = user.uuid
    else:
        data[STATUS] = LOGIN_FAILED
    return json.dumps(data)