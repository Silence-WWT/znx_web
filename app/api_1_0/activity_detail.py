# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import Activity, ActivityComment, Age
from . import api
from api_constants import *


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
            'start_time': str(activity.start_time),
            'end_time': str(activity.end_time),
            'comments_count': comments_count
        }
        data['status'] = SUCCESS
    else:
        data['status'] = ACTIVITY_NOT_EXIST
    return json.dumps(data)