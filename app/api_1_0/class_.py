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
    try:
        page = int(request.args.get('page'))
    except TypeError:
        page = 1
    except ValueError:
        data['status'] = PARAMETER_ERROR
        return json.dumps(data)
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
    class_ = Class.query.get(class_id)
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
    try:
        address = request.args.get('address').encode('utf8')
        name = request.args.get('name').encode('utf8')
    except AttributeError:
        data['status'] = LACK_OF_PARAMETER
        return json.dumps(data)
    remark = request.args.get('remark')
    if remark:
        remark = remark.encode('utf8')
    class_id = request.args.get('class')
    mobile = request.args.get('mobile')
    age = request.args.get('age')
    sex = request.args.get('sex')
    email = request.args.get('email')
    time = request.args.get('time')

    class_ = Class.query.get(class_id)
    user = User.query.get(user_id)
    if class_ and user and age and mobile and sex and time and email:
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
        try:
            db.session.add(class_order)
            db.session.commit()
        except Exception:
            data['status'] = SQL_EXCEPTION
        else:
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
    stars = request.args.get('stars')
    user = User.query.get(user_id)
    class_ = Class.query.filter_by(id=class_id).first()
    if user and class_ and u'1' <= stars <= u'5' and len(stars) == 1:
        class_comment_ = ClassComment(
            class_id=class_.id,
            user_id=user.id,
            stars=stars,
            body=comment,
            created=time_now()
        )
        try:
            db.session.add(class_comment_)
            db.session.commit()
        except Exception:
            data['status'] = SQL_EXCEPTION
        else:
            data['status'] = SUCCESS
    elif not class_:
        data['status'] = ACTIVITY_NOT_EXIST
    else:
        data['status'] = PARAMETER_ERROR
    return json.dumps(data)


@api.route('/class_comment_list')
def class_comment_list():
    data = {'class_comments': []}
    try:
        page = int(request.args.get('page'))
    except TypeError:
        page = 1
    except ValueError:
        data['status'] = PARAMETER_ERROR
        return json.dumps(data)
    class_id = request.args.get('class')
    class_ = Class.query.filter_by(id=class_id).first()
    if class_:
        comment_list = ClassComment.query.filter_by(class_id=class_id).paginate(page, PER_PAGE, False).items
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