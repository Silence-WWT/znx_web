# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import User
from . import api
from api_constants import *


@api.route('/login')
def login():
    data = {}
    username = request.args.get('username')
    password = request.args.get('password')
    # TODO: 如果用户名恰好是另一个用户的手机号，可能会导致登陆错误
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User.query.filter_by(cellphone=username).first()
    if user is not None and user.verify_password(password):
        # user.update_uuid(request.args.get('uuid'))
        # 待数据库表建完整后再适当修改
        # TODO: update uuid.
        data[STATUS] = SUCCESS
    else:
        data[STATUS] = LOGIN_FAILED
    return json.dumps(data)