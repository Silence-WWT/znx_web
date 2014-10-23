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
    identity = request.args.get('identity')
    email = request.args.get('email')
    if User.query.filter_by(cellphone=cellphone).first():
        data['status'] = CELLPHONE_EXIST
        return json.dumps(data)
    elif User.query.filter_by(username=username).first():
        data['status'] = USERNAME_EXIST
        return json.dumps(data)
    if username and password and cellphone:
        user = User(
            username=username,
            password=password,
            cellphone=cellphone,
            identity=identity
        )
        if email:
            user.email = email
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
                'cellphone': cellphone,
                'identity': identity,
                'email': email
            }
    return json.dumps(data)