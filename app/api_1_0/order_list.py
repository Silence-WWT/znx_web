# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import User, Organization, Class, ClassOrder, Activity, ActivityOrder
from . import api
from api_constants import *


@api.route('/order_list')
def order_list():
    data = {}
    mobile = request.args.get('mobile')
    username = request.args.get('username')
    try:
        page = int(request.args.get('page'))
    except TypeError:
        page = 1
    except ValueError:
        data['status'] = PARAMETER_ERROR
        return json.dumps(data)
    user = User.query.filter_by(username=username, mobile=mobile).first()
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
                'created': str(class_order.created),
                'class_name': class_.name,
                'org_name': org.name,
            }
            orders_list.append(class_dict)
        for activity_order in activity_orders:
            activity = Activity.query.get(activity_order.activity_id)
            org = Organization.query.get(activity.organization_id)
            activity_dict = {
                'activity_order_id': activity_order.id,
                'created': str(activity_order.created),
                'activity_name': activity.name,
                'org_name': org.name,
            }
            orders_list.append(activity_dict)
        data['orders'] = sorted(orders_list, key=lambda x: x['created'], reverse=True)
        data['status'] = SUCCESS
    else:
        data['status'] = USER_NOT_EXIST
    return json.dumps(data)