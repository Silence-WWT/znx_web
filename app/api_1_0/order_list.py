# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import User, Organization, Class, ClassOrder, Activity, ActivityOrder
from . import api
from api_constants import *


@api.route('/order_list')
def order_list():
    data = {}
    cellphone = request.args.get('cellphone')
    username = request.args.get('username')
    try:
        page = int(request.args.get('page'))
    except TypeError:
        page = 1
    except ValueError:
        data['status'] = PARAMETER_ERROR
        return json.dumps(data)
    user = User.query.filter_by(username=username, cellphone=cellphone).first()
    if user:
        orders_list = []
        class_orders = ClassOrder.query.filter_by(user_id=user.id)\
            .order_by(-ClassOrder.timestamp)\
            .paginate(page, PER_PAGE, False).items
        activity_orders = ActivityOrder.query.filter_by(user_id=user.id)\
            .order_by(-ActivityOrder.timestamp)\
            .paginate(page, PER_PAGE, False).items
        for class_order in class_orders:
            class_ = Class.query.filter_by(id=class_order.class_id).first()
            org = Organization.query.filter_by(id=class_.organization_id).first()
            class_dict = {
                'class_order_id': class_order.id,
                'timestamp': str(class_order.timestamp),
                'class_name': class_.name,
                'org_name': org.name,
            }
            orders_list.append(class_dict)
        for activity_order in activity_orders:
            activity = Activity.query.filter_by(id=activity_order.activity_id).first()
            org = Organization.query.filter_by(id=activity.organization_id).first()
            activity_dict = {
                'activity_order_id': activity_order.id,
                'timestamp': str(activity_order.timestamp),
                'activity_name': activity.name,
                'org_name': org.name,
            }
            orders_list.append(activity_dict)
        data['orders'] = sorted(orders_list, key=lambda x: x['timestamp'], reverse=True)
        data['status'] = SUCCESS
    else:
        data['status'] = USER_NOT_EXISTS
    return json.dumps(data)