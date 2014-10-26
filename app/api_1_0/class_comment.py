# -*- coding: utf-8 -*-
import json
from time import time as time_now

from flask import request

from app import db
from ..models import User, Class, ClassComment
from . import api
from api_constants import *


@api.route('/class_comment')
def class_comment():
    data = {}
    username = request.args.get('username')
    class_id = request.args.get('class')
    comment = request.args.get('comment')
    stars = request.args.get('stars')
    user = User.query.filter_by(username=username).first()
    class_ = Class.query.filter_by(id=class_id).first()
    if user and class_ and comment and u'1' <= stars <= u'5' and len(stars) == 1:
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
