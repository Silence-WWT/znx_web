# -*- coding: utf-8 -*-
import json
import time

from flask import request

from app import db
from ..models import User, Activity, ActivityComment, ActivityOrder, Category
from . import api
from api_constants import *
from utils import get_ages, get_unified


@api.route('/activity_list')
def activity_list():
    data = {'activities': []}
    page = request.values.get('page', 1, type=int)
    organization_id = request.values.get('organization')
    activity_list_ = Activity.query.filter_by(organization_id=organization_id).paginate(page, PER_PAGE, False).items
    for activity in activity_list_:
        activity_dict = {
            'id': activity.id,
            'name': activity.name,
            'age': get_ages(activity),
            'price': activity.price,
            'start_time': activity.start_time,
            'end_time': activity.end_time
        }
        data['activities'].append(activity_dict)
    data['status'] = SUCCESS
    return json.dumps(data)


@api.route('/activity_detail')
def activity_detail():
    data = {'activity': {}}
    activity_id = request.values.get('activity')
    activity = Activity.query.get(activity_id)
    if activity:
        category = Category.query.get(activity.category_id)
        data['activity'] = {
            'id': activity.id,
            'name': activity.name,
            'age': get_ages(activity),
            'price': activity.price,
            'intro': activity.detail,
            'start_time': activity.start_time,
            'end_time': activity.end_time,
            'comments_count': activity.get_comment_count(),
            'landmark': activity.landmark,
            'address': activity.address,
            'traffic': activity.traffic,
            'contract_phone': activity.contract_phone,
            'category': category.category,
            'stars': activity.stars
        }
        data['status'] = SUCCESS
    else:
        data['status'] = ACTIVITY_NOT_EXIST
    return json.dumps(data)


@api.route('/activity_sign_up')
def activity_sign_up():
    data = {}
    activity_id = request.values.get('activity', '', type=str)
    user_id = request.values.get('user_id')
    uuid = request.values.get('uuid', '', type=str)
    address = request.values.get('address', u'', type=unicode)
    name = request.values.get('name', u'', type=unicode)
    remark = request.values.get('remark', u'', type=unicode)
    mobile = request.values.get('mobile', '', type=str)
    age = request.values.get('age', '', type=str)
    sex = request.values.get('sex', '', type=str)
    email = request.values.get('email', '', type=str)
    activity = Activity.query.get(activity_id)
    if activity and age and mobile:
        activity.get_org().add_orders()
        unified = get_unified(user_id, uuid)
        activity_order = ActivityOrder(
            activity_id=activity_id,
            unified_id=unified.id,
            name=name,
            mobile=mobile,
            age=age,
            sex=sex,
            email=email,
            address=address,
            remark=remark,
            created=time.time(),
            is_submitted=True,
            is_canceled=False
        )
        db.session.add(activity_order)
        db.session.commit()
        data['status'] = SUCCESS
    else:
        data['status'] = LACK_OF_PARAMETER
    return json.dumps(data)


@api.route('/activity_comment')
def activity_comment():
    data = {}
    activity_id = request.values.get('activity')
    stars = request.values.get('stars', 0, type=int)
    user_id = request.values.get('user_id')
    comment = request.values.get('comment', u'', type=unicode)
    user = User.query.get(user_id)
    activity = Activity.query.get(activity_id)
    if user and activity and 1 <= stars <= 5:
        activity_comment_ = ActivityComment(
            activity_id=activity.id,
            user_id=user.id,
            stars=stars,
            body=comment,
            created=time.time()
        )
        db.session.add(activity_comment_)
        db.session.commit()
        data['status'] = SUCCESS
    elif not activity:
        data['status'] = ACTIVITY_NOT_EXIST
    else:
        data['status'] = PARAMETER_ERROR
    return json.dumps(data)


@api.route('/activity_comment_list')
def activity_comment_list():
    data = {'activity_comments': []}
    page = request.values.get('page', 1, type=int)
    activity_id = request.values.get('activity')
    activity = Activity.query.get(activity_id)
    if activity:
        comment_list = ActivityComment.query.\
            filter_by(activity_id=activity_id).\
            order_by(-ActivityComment.created).\
            paginate(page, PER_PAGE, False).items
        for comment in comment_list:
            user = User.query.get(comment.user_id)
            comment_dict = {
                'body': comment.body,
                'stars': comment.stars,
                'created': comment.created,
                'username': user.username
            }
            data['activity_comments'].append(comment_dict)
        data['status'] = SUCCESS
    else:
        data['status'] = CLASS_NOT_EXIST
    return json.dumps(data)