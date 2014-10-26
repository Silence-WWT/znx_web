# -*- coding: utf-8 -*-
import json
from time import time as time_now

from flask import request

from app import db
from ..models import User, Class, ClassOrder
from . import api
from api_constants import *


@api.route('/class_sign_up')
def class_sign_up():
    data = {}
    class_id = request.args.get('class')
    username = request.args.get('username')
    mobile = request.args.get('mobile')
    name = request.args.get('name')
    age = request.args.get('age')
    sex = request.args.get('sex')
    email = request.args.get('email')
    address = request.args.get('address')
    remark = request.args.get('remark')
    time = request.args.get('time')

    class_ = Class.query.filter_by(id=class_id).first()
    user = User.query.filter_by(username=username).first()
    if class_ and user and name and age and mobile and sex and address and time and email:
        class_order = ClassOrder(
            class_id=class_id,
            user_id=user.id,
            name=name,
            mobile=mobile,
            age=age,
            sex=sex,
            email=email,
            address=address,
            remark=remark,
            time=time,
            campus=u'',
            created=time_now()
        )
        try:
            db.session.add(class_order)
            db.session.commit()
        except Exception:
            data['status'] = SQL_EXCEPTION
        else:
            data['status'] = SUCCESS
    else:
        data['status'] = LACK_OF_PARAMETER
    return json.dumps(data)