# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import Activity, Age
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