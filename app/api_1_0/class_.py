# -*- coding: utf-8 -*-
import json
import time

from flask import request

from app import db
from ..models import User, Class, ClassComment, ClassOrder
from . import api
from api_constants import *
from utils import get_ages, get_unified


@api.route('/class_list')
def class_list():
    data = {'classes': []}
    page = request.values.get('page', 1, type=int)
    organization_id = request.args.get('organization')
    class_list_ = Class.query.filter_by(organization_id=organization_id).paginate(page, PER_PAGE, False).items
    for class_ in class_list_:
        class_dict = {
            'id': class_.id,
            'name': class_.name,
            'age': get_ages(class_),
            'price': class_.price,
            'days': class_.days
        }
        data['classes'].append(class_dict)
    data['status'] = SUCCESS
    return json.dumps(data)


@api.route('/class_detail')
def class_detail():
    data = {'class': {}}
    class_id = request.args.get('class')
    class_ = Class.query.filter_by(id=class_id).first()
    if class_:
        data['class'] = {
            'id': class_.id,
            'name': class_.name,
            'age': get_ages(class_),
            'price': class_.price,
            'intro': class_.detail,
            'consult_time': class_.consult_time,
            'is_round': class_.is_round,
            'is_tastable': class_.is_tastable,
            'comments_count': class_.get_comment_count(),
            'days': class_.days,
            'stars': class_.stars
        }
        data['status'] = SUCCESS
    else:
        data['status'] = CLASS_NOT_EXIST
    return json.dumps(data)


@api.route('/class_sign_up')
def class_sign_up():
    data = {}
    user_id = request.args.get('user_id')
    uuid = request.args.get('uuid')
    address = request.args.get('address', u'', type=unicode)
    name = request.args.get('name', u'', type=unicode)
    remark = request.args.get('remark', u'', type=unicode)
    class_id = request.args.get('class')
    mobile = request.args.get('mobile')
    age = request.args.get('age')
    sex = request.args.get('sex')
    email = request.args.get('email')
    taste_time = request.args.get('time')

    class_ = Class.query.filter_by(id=class_id).first()
    if class_ and name and address and age and mobile and sex and taste_time and email:
        class_.get_org().add_orders()
        unified = get_unified(user_id, uuid)
        class_order = ClassOrder(
            class_id=class_id,
            unified_id=unified.id,
            name=name,
            mobile=mobile,
            age=age,
            sex=sex,
            email=email,
            address=address,
            remark=remark,
            time=taste_time,
            created=time.time(),
            is_canceled=False,
            is_submitted=True
        )
        db.session.add(class_order)
        db.session.commit()
        data['status'] = SUCCESS
    else:
        data['status'] = LACK_OF_PARAMETER
    return json.dumps(data)


@api.route('/class_comment')
def class_comment():
    data = {}
    user_id = request.args.get('user_id')
    comment = request.args.get('comment', u'', type=unicode)
    class_id = request.args.get('class')
    stars = request.values.get('stars', 0, type=int)
    user = User.query.filter_by(id=user_id).first()
    class_ = Class.query.filter_by(id=class_id).first()
    if user and class_ and 1 <= stars <= 5:
        class_comment_ = ClassComment(
            class_id=class_.id,
            user_id=user.id,
            stars=stars,
            body=comment,
            created=time.time()
        )
        db.session.add(class_comment_)
        db.session.commit()
        data['status'] = SUCCESS
    elif not class_:
        data['status'] = ACTIVITY_NOT_EXIST
    else:
        data['status'] = PARAMETER_ERROR
    return json.dumps(data)


@api.route('/class_comment_list')
def class_comment_list():
    data = {'class_comments': []}
    page = request.values.get('page', 1, type=int)
    class_id = request.args.get('class')
    class_ = Class.query.filter_by(id=class_id).first()
    if class_:
        comment_list = ClassComment.query.filter_by(class_id=class_id).\
            order_by(-ClassComment.created).\
            paginate(page, PER_PAGE, False).items
        for comment in comment_list:
            user = User.query.get(comment.user_id)
            comment_dict = {
                'body': comment.body,
                'stars': comment.stars,
                'created': comment.created,
                'username': user.username
            }
            data['class_comments'].append(comment_dict)
        data['status'] = SUCCESS
    else:
        data['status'] = CLASS_NOT_EXIST
    return json.dumps(data)