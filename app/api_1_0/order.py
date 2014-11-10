# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import User, Organization, Class, ClassOrder, Activity, ActivityOrder, UnifiedId
from . import api
from api_constants import *
from utils import get_ages


@api.route('/order_list_or_detail')
def order_list():
    data = {}
    user_id = request.values.get('user_id', '', type=str)
    uuid = request.values.get('uuid', '', type=str)
    page = request.values.get('page', 1, type=int)
    unified_user_id = list(UnifiedId.query.filter_by(user_id=user_id))
    unified_uuid = list(UnifiedId.query.filter_by(mobile_key=uuid))
    unified_list = []
    unified_list.extend(unified_user_id)
    unified_list.extend(unified_uuid)
    unified_id_list = [unified.id for unified in unified_list]
    if unified_id_list:
        class_order_list = []
        class_orders = ClassOrder.query.\
            filter(UnifiedId.id.in_(unified_id_list)).\
            order_by(-ClassOrder.created).\
            paginate(page, PER_PAGE, False).items
        for class_order in class_orders:
            class_dict = get_order_dict('class', class_order)
            class_order_list.append(class_dict)

        activity_order_list = []
        activity_orders = ActivityOrder.query.\
            filter(UnifiedId.id.in_(unified_id_list)).\
            order_by(-ActivityOrder.created).\
            paginate(page, PER_PAGE, False).items
        for activity_order in activity_orders:
            activity_dict = get_order_dict('activity', activity_order)
            activity_order_list.append(activity_dict)

        data['activity_orders'] = sorted(activity_order_list, key=lambda x: x['created'], reverse=True)
        data['class_orders'] = sorted(class_order_list, key=lambda x: x['created'], reverse=True)
    data['status'] = SUCCESS
    return json.dumps(data)


@api.route('/order_synchronize')
def order_synchronize():
    data = {}
    user_id = request.args.get('user_id')
    uuid = request.args.get('uuid')
    if not User.query.filter_by(id=user_id).first():
        data['status'] = USER_NOT_EXIST
    else:
        order_profile_list = UnifiedId.query.filter_by(mobile_key=uuid, user_id='')
        for order_profile in order_profile_list:
            order_profile.user_id = user_id
        data['status'] = SUCCESS
    return json.dumps(data)


def get_order_dict(order_type, order):
    if isinstance(order, ClassOrder):
        obj = Class.query.get(order.class_id)
    else:
        obj = Activity.query.get(order.activity_id)
    org = Organization.query.get(obj.organization_id)
    order_dict = {
        order_type + '_order_id': order.id,
        order_type + '_name': order.name,
        'org_name': org.name,
        'created': order.created,
        'price': obj.price,
        'age': get_ages(obj),
        'user_name': order.name,
        'user_age': order.age,
        'user_sex': order.sex,
        'user_mobile': order.mobile,
        'user_email': order.email,
        'user_address': order.address,
        'user_remark': order.remark,
        'comments_count': obj.get_comment_count()
    }
    if isinstance(order, ClassOrder):
        order_dict['days'] = obj.days
    else:
        order_dict['start_time'] = obj.start_time
        order_dict['end_time'] = obj.end_time
    return order_dict