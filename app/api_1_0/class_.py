# -*- coding: utf-8 -*-
import json
from time import time as time_now

from flask import request

from app import db
from ..models import User, Class, ClassComment, ClassOrder, Age
from . import api
from api_constants import *


@api.route('/class_list')
def class_list():
    data = {'classes': []}
    page = request.values.get('page', 1, type=int)
    organization_id = request.args.get('organization')
    class_list_ = Class.query.filter_by(organization_id=organization_id).paginate(page, PER_PAGE, False).items
    for class_ in class_list_:
        age = Age.query.get(class_.age_id)
        class_dict = {
            'id': class_.id,
            'name': class_.name,
            'age': age.age,
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
        age = Age.query.get(class_.age_id)
        comments_count = ClassComment.query.filter_by(class_id=class_.id).count()
        data['class'] = {
            'id': class_.id,
            'name': class_.name,
            'age': age.age,
            'price': class_.price,
            'intro': class_.intro,
            'consult_time': class_.consult_time,
            'is_round': class_.is_round,
            'is_tastable': class_.is_tastable,
            'comments_count': comments_count,
            'days': class_.days
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
    address = request.args.get('address', '').encode('utf8')
    name = request.args.get('name', '').encode('utf8')
    remark = request.args.get('remark', '').encode('utf8')
    class_id = request.args.get('class')
    mobile = request.args.get('mobile')
    age = request.args.get('age')
    sex = request.args.get('sex')
    email = request.args.get('email')
    time = request.args.get('time')

    class_ = Class.query.filter_by(id=class_id).first()
    if class_ and age and mobile and sex and time and email:
        order_profile = OrderProfile(
            user_id=user_id,
            mobile_uuid=uuid,
            web_uuid=''
        )
        db.session.add(order_profile)
        db.session.commit()
        class_order = ClassOrder(
            class_id=class_id,
            order_profile_id=order_profile.id,
            name=name,
            mobile=mobile,
            age=age,
            sex=sex,
            email=email,
            address=address,
            remark=remark,
            time=time,
            campus=u'',
            created=time_now()
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
    try:
        comment = request.args.get('comment').encode('utf8')
    except AttributeError:
        data['status'] = LACK_OF_PARAMETER
        return json.dumps(data)
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
            created=time_now()
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