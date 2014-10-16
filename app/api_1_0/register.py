# -*- coding: utf-8 -*-
import json

from flask import request

from app import db
from ..models import User
from . import api
from api_constants import *


@api.route('/register')
def register():
    data = {}
    username = request.args.get('username')
    password = request.args.get('password')
    cellphone = request.args.get('cellphone')
    if User.query.filter_by(username=username).first():
        data[STATUS] = USERNAME_EXISTS
    else:
        user = User()
        user.username = username
        user.password = password
        user.cellphone = cellphone
        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            data[STATUS] = SQL_EXCEPTION
        else:
            data[STATUS] = SUCCESS
    return json.dumps(data)