# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import User, Class, ClassOrder, Activity, ActivityOrder
from . import api
from api_constants import *


@api.route('/order_detail')
def order_detail():
    data = {}
    username = request.args.get('username')
    mobile = request.args.get('mobile')
    class_order_id = request.args.get('class_order')
    user = User.query.filter_by(username=username, mobile=mobile).first()
    if user:
        if class_order_id:
            order = ClassOrder.query.filter_by(id=class_order_id).first()
        else:
            activity_order_id = request.args.get('activity_order')
            order = ActivityOrder.query.filter_by(id=activity_order_id).first()
        if not order:
            data['status'] = ORDER_NOT_EXIST
            return json.dumps(data)
        elif user.id != order.user_id:
            data['status'] = ACCESS_RESTRICTED
            return json.dumps(data)
        order_dict = {
            'created': str(order.created),
            'name': order.name,
            'age': order.age,
            'sex': order.sex,
            'mobile': order.mobile,
            'address': order.address,
            'remark': order.remark
        }
        if class_order_id:
            class_ = Class.query.filter_by(id=order.class_id).first()
            order_dict['class_name'] = class_.name
            order_dict['time'] = str(order.time)
            data['class_order'] = order_dict
        else:
            activity = Activity.query.filter_by(id=order.activity_id).first()
            order_dict['activity_name'] = activity.name
            data['activity_order'] = order_dict
        data['status'] = SUCCESS
    else:
        data['status'] = USER_NOT_EXIST
    return json.dumps(data)