# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import User, Organization, Class, ClassOrder, Activity, ActivityOrder
from . import api
from api_constants import *


@api.route('/order_list')
def order_list():
    data = {}
    user_id = request.args.get('user_id')
    try:
        page = int(request.args.get('page'))
    except TypeError:
        page = 1
    except ValueError:
        data['status'] = PARAMETER_ERROR
        return json.dumps(data)
    user = User.query.get(user_id)
    if user:
        orders_list = []
        class_orders = ClassOrder.query.filter_by(user_id=user.id)\
            .order_by(-ClassOrder.created)\
            .paginate(page, PER_PAGE, False).items
        activity_orders = ActivityOrder.query.filter_by(user_id=user.id)\
            .order_by(-ActivityOrder.created)\
            .paginate(page, PER_PAGE, False).items
        for class_order in class_orders:
            class_ = Class.query.get(class_order.class_id)
            org = Organization.query.get(class_.organization_id)
            class_dict = {
                'class_order_id': class_order.id,
                'created': class_order.created,
                'class_name': class_.name,
                'org_name': org.name,
            }
            orders_list.append(class_dict)
        for activity_order in activity_orders:
            activity = Activity.query.get(activity_order.activity_id)
            org = Organization.query.get(activity.organization_id)
            activity_dict = {
                'activity_order_id': activity_order.id,
                'created': activity_order.created,
                'activity_name': activity.name,
                'org_name': org.name,
            }
            orders_list.append(activity_dict)
        data['orders'] = sorted(orders_list, key=lambda x: x['created'], reverse=True)
        data['status'] = SUCCESS
    else:
        data['status'] = USER_NOT_EXIST
    return json.dumps(data)


@api.route('/class_order_detail')
def class_order_detail():
    data = {}
    user_id = request.args.get('user_id')
    class_order_id = request.args.get('class_order')
    user = User.query.get(user_id)
    if user:
        class_order = ClassOrder.query.get(class_order_id)
        if not class_order:
            data['status'] = ORDER_NOT_EXIST
            return json.dumps(data)
        elif user.id != class_order.user_id:
            data['status'] = ACCESS_RESTRICTED
            return json.dumps(data)
        class_ = Class.query.get(class_order.class_id)
        data['class_order'] = {
            'class_name': class_.name,
            'created': class_order.created,
            'name': class_order.name,
            'age': class_order.age,
            'sex': class_order.sex,
            'email': class_order.email,
            'time': class_.time,
            'mobile': class_order.mobile,
            'address': class_order.address,
            'remark': class_order.remark
        }
        data['status'] = SUCCESS
    else:
        data['status'] = USER_NOT_EXIST
    return json.dumps(data)


@api.route('/activity_order_detail')
def activity_order_detail():
    data = {}
    user_id = request.args.get('user_id')
    activity_order_id = request.args.get('activity_order')
    user = User.query.get(user_id)
    if user:
        activity_order = ActivityOrder.query.get(activity_order_id)
        if not activity_order:
            data['status'] = ORDER_NOT_EXIST
            return json.dumps(data)
        elif user.id != activity_order.user_id:
            data['status'] = ACCESS_RESTRICTED
            return json.dumps(data)
        activity = Activity.query.get(activity_order.activity_id)
        data['activity_order'] = {
            'activity_name': activity.name,
            'created': activity_order.created,
            'name': activity_order.name,
            'age': activity_order.age,
            'sex': activity_order.sex,
            'mobile': activity_order.mobile,
            'email': activity_order.email,
            'address': activity_order.address,
            'remark': activity_order.remark
        }
        data['status'] = SUCCESS
    else:
        data['status'] = USER_NOT_EXIST
    return json.dumps(data)


@api.route('/order_synchronize')
def order_synchronize():
    data = {}
    user_id = request.args.get('user_id')
    uuid = request.args.get('uuid')
    if not User.query.get(user_id):
        data['status'] = USER_NOT_EXIST
    else:
        order_profile_list = OrderProfile.query.filter_by(uuid=uuid, user_id='')
        for order_profile in order_profile_list:
            order_profile.user_id = user_id
        data['status'] = SUCCESS
    return json.dumps(data)