# -*- coding: utf-8 -*-
import json
from datetime import datetime

from flask import request

from app import db
from ..models import User, Activity, ActivityComment
from . import api
from api_constants import *


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
            timestamp=datetime.now()
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
