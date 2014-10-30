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
        age = Age.query.get(activity.age_id)
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
        age = Age.query.get(activity.age_id)
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
    user_id = request.args.get('user_id')
    uuid = request.args.get('uuid')
    try:
        name = request.args.get('name').encode('utf8')
        address = request.args.get('address').encode('utf8')
    except AttributeError:
        data['status'] = LACK_OF_PARAMETER
        return json.dumps(data)
    remark = request.args.get('remark')
    if remark:
        remark = remark.encode('utf8')
    mobile = request.args.get('mobile')
    age = request.args.get('age')
    sex = request.args.get('sex')
    email = request.args.get('email')

    activity = Activity.query.get(activity_id)
    user = User.query.get(user_id)
    if activity and user and age and mobile and sex:
        order_profile = OrderProfile(
            user_id=user_id,
            mobile_uuid=uuid,
            web_uuid=''
        )
        db.session.add(order_profile)
        db.session.commit()
        activity_order = ActivityOrder(
            activity_id=activity_id,
            order_profile_id=order_profile.id,
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
    activity_id = request.args.get('activity')
    stars = request.args.get('stars')
    user_id = request.args.get('user_id')
    try:
        comment = request.args.get('comment').encode('utf8')
    except AttributeError:
        data['status'] = LACK_OF_PARAMETER
        return json.dumps(data)
    user = User.query.get(user_id)
    activity = Activity.query.get(activity_id)
    if user and activity and u'1' <= stars <= u'5' and len(stars) == 1:
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