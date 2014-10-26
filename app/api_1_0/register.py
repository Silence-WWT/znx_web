# -*- coding: utf-8 -*-
import json
from time import time as time_now

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
    mobile = request.args.get('mobile')
    identity = request.args.get('identity')
    email = request.args.get('email')
    if User.query.filter_by(mobile=mobile).first():
        data['status'] = CELLPHONE_EXIST
        return json.dumps(data)
    elif User.query.filter_by(username=username).first():
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
            created=time_now()
        )
        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            data['status'] = SQL_EXCEPTION
        else:
            data['status'] = SUCCESS
            data['user'] = {
                'username': username,
                'mobile': mobile,
                'identity': identity,
                'email': email
            }
    return json.dumps(data)