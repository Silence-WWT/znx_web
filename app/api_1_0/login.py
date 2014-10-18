# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import User, Class_Order, Activity_Order, Class, Activity, Organization
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
        if user.identity != identity:
            user.identity = identity
        data[STATUS] = SUCCESS
        data['user'] = {
            'username': user.username,
            'cellphone': user.cellphone,
            'email': user.email,
            'identity': user.identity
        }
        data['classes'] = []
        data['activities'] = []
        class_orders = Class_Order.query.filter_by(user_id=user.id)
        activity_orders = Activity_Order.query.filter_by(user_id=user.id)
        for class_order in class_orders:
            class_ = Class.query.join(Class_Order).filter_by(Class.id == Class_Order.class_id).first()
            org = Organization.query.join(Class).filter_by(Organization.id == Class.organization_id).first()
            class_dict = {
                'time': class_order.time,
                'timestamp': class_order.timestamp,
                'class_name': class_.name,
                'org_name': org.name,
                'name': class_order.name,
                'age': class_order.age,
                'sex': class_order.sex,
                'cellphone': class_order.cellphone,
                'address': class_order.address,
                'remark': class_order.remark
            }
            data['classes'].append(class_dict)
        for activity_order in activity_orders:
            activity = Activity.query.join(Activity_Order).filter_by(Activity.id == Activity_Order.activity_id).first()
            org = Organization.query.join(Activity).filter_by(Organization.id == Activity.organization_id).first()
            activity_dict = {
                'timestamp': activity_order.timestamp,
                'activity_name': activity.name,
                'org_name': org.name,
                'name': activity_order.name,
                'age': activity_order.age,
                'sex': activity_order.sex,
                'cellphone': activity_order.cellphone,
                'address': activity_order.address,
                'remark': activity_order.remark
            }
            data['activities'].append(activity_dict)
    else:
        data[STATUS] = LOGIN_FAILED
    return json.dumps(data)