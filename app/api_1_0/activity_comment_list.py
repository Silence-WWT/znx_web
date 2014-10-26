# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import User, Activity, ActivityComment
from . import api
from api_constants import *


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
                'created': str(comment.created),
                'username': user.username
            }
            data['activity_comments'].append(comment_dict)
        data['status'] = SUCCESS
    else:
        data['status'] = CLASS_NOT_EXIST
    return json.dumps(data)