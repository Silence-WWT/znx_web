# -*- coding: utf-8 -*-
import json
import time

from flask import request

from app import db
from ..models import User, Activity, ActivityComment, ActivityOrder, Category
from . import api
from api_constants import *
from helper import get_ages, get_unified


@api.route('/activity_list')
def activity_list():
    data = {'activities': []}
    page = request.values.get('page', 1, type=int)
    organization_id = request.args.get('organization')
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
    activity_id = request.args.get('activity')
    activity = Activity.query.filter_by(id=activity_id).first()
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
            'category': category.category
        }
        data['status'] = SUCCESS
    else:
        data['status'] = ACTIVITY_NOT_EXIST
    return json.dumps(data)


@api.route('/activity_sign_up')
def activity_sign_up():
    data = {}
    activity_id = request.args.get('activity')
    user_id = request.args.get('user_id')
    uuid = request.args.get('uuid')
    address = request.args.get('address', u'', type=unicode)
    name = request.args.get('name', u'', type=unicode)
    remark = request.args.get('remark', u'', type=unicode)
    mobile = request.args.get('mobile')
    age = request.args.get('age')
    sex = request.args.get('sex')
    email = request.args.get('email')

    activity = Activity.query.filter_by(id=activity_id).first()
    if activity and age and mobile:
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
    activity_id = request.args.get('activity')
    stars = request.values.get('stars', 0, type=int)
    user_id = request.args.get('user_id')
    comment = request.args.get('comment', '').encode('utf8')
    user = User.query.filter_by(id=user_id).first()
    activity = Activity.query.filter_by(id=activity_id).first()
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
    activity_id = request.args.get('activity')
    activity = Activity.query.filter_by(id=activity_id).first()
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