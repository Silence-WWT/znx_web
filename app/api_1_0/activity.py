# -*- coding: utf-8 -*-
import json
from time import time as time_now

from flask import request

from app import db
from ..models import User, Activity, ActivityComment, ActivityOrder, Age
from . import api
from api_constants import *


@api.route('/activity_list')
def activity_list():
    data = {'activities': []}
    try:
        page = int(request.args.get('page'))
    except TypeError:
        page = 1
    except ValueError:
        data['status'] = PARAMETER_ERROR
        return json.dumps(data)
    organization_id = request.args.get('organization')
    activity_list_ = Activity.query.filter_by(organization_id=organization_id).paginate(page, PER_PAGE, False).items
    for activity in activity_list_:
        age = Age.query.filter_by(id=activity.age_id).first()
        activity_dict = {
            'id': activity.id,
            'name': activity.name,
            'age': age.age,
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
        age = Age.query.filter_by(id=activity.age_id).first()
        comments_count = ActivityComment.query.filter_by(activity_id=activity.id).count()
        data['activity'] = {
            'id': activity.id,
            'name': activity.name,
            'age': age.age,
            'price': activity.price,
            'intro': activity.intro,
            'start_time': activity.start_time,
            'end_time': activity.end_time,
            'comments_count': comments_count
        }
        data['status'] = SUCCESS
    else:
        data['status'] = ACTIVITY_NOT_EXIST
    return json.dumps(data)


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
    if activity and user and name and age and mobile and sex and address:
        activity_order = ActivityOrder(
            activity_id=activity_id,
            user_id=user.id,
            name=name,
            mobile=mobile,
            age=age,
            sex=sex,
            email=email,
            address=address,
            remark=remark,
            created=time_now(),
            is_submitted=True,
            is_canceled=False
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


@api.route('/activity_comment')
def activity_comment():
    data = {}
    username = request.args.get('username')
    activity_id = request.args.get('activity')
    comment = request.args.get('comment')
    stars = request.args.get('stars')
    user = User.query.filter_by(username=username).first()
    activity = Activity.query.filter_by(id=activity_id).first()
    if user and activity and comment and u'1' <= stars <= u'5' and len(stars) == 1:
        activity_comment_ = ActivityComment(
            activity_id=activity.id,
            user_id=user.id,
            stars=stars,
            body=comment,
            created=time_now()
        )
        try:
            db.session.add(activity_comment_)
            db.session.commit()
        except Exception:
            data['status'] = SQL_EXCEPTION
        else:
            data['status'] = SUCCESS
    elif not activity:
        data['status'] = ACTIVITY_NOT_EXIST
    else:
        data['status'] = PARAMETER_ERROR
    return json.dumps(data)


@api.route('/activity_comment_list')
def activity_comment_list():
    data = {'activity_comments': []}
    try:
        page = int(request.args.get('page'))
    except TypeError:
        page = 1
    except ValueError:
        data['status'] = PARAMETER_ERROR
        return json.dumps(data)
    activity_id = request.args.get('activity')
    activity = Activity.query.filter_by(id=activity_id).first()
    if activity:
        comment_list = ActivityComment.query.filter_by(activity_id=activity_id).paginate(page, PER_PAGE, False).items
        for comment in comment_list:
            user = User.query.filter_by(id=comment.user_id).first()
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