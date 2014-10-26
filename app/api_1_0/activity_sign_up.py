# -*- coding: utf-8 -*-
import json
from datetime import datetime

from flask import request

from app import db
from ..models import User, Activity, ActivityOrder
from . import api
from api_constants import *


@api.route('/activity_sign_up')
def activity_sign_up():
    data = {}
    activity_id = request.args.get('activity')
    username = request.args.get('username')
    mobile = request.args.get('mobile')
    name = request.args.get('name')
    age = request.args.get('age')
    sex = request.args.get('sex')
    email = request.args.get('email')
    address = request.args.get('address')
    remark = request.args.get('remark')

    activity = Activity.query.filter_by(id=activity_id).first()
    user = User.query.filter_by(username=username).first()
    if activity and user and name and age and mobile and sex and address and remark:
        activity_order = ActivityOrder(
            class_id=activity_id,
            user_id=user.id,
            name=name,
            mobile=mobile,
            age=age,
            sex=sex,
            email=email,
            address=address,
            remark=remark,
            created=datetime.now()
        )
        try:
            db.session.add(activity_order)
            db.session.commit()
        except Exception:
            data['status'] = SQL_EXCEPTION
        else:
            data['status'] = SUCCESS
    else:
        data['status'] = LACK_OF_PARAMETER
    return json.dumps(data)