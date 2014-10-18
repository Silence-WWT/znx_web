# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import Organization, Class, Activity
from . import api
from api_constants import *


@api.route('/organization_detail')
def organization_detail():
    data = {}
    org_id = request.args.get('organization')
    organization = Organization.query.filter_by(id=org_id).first()
    if organization:
        data = {STATUS: SUCCESS, 'classes': [], 'activities': []}
        org_dict = {
            'id': organization.id,
            'name': organization.name,
            'photo': organization.photo.url,
            'location': organization.location.district,
            'intro': organization.intro,
            'address': organization.address,
            'cellphone': organization.cellphone,
            'comments_count': organization.comments.count()
        }
        data['organization'] = org_dict
        class_list = list(Class.query.filter_by(organization_id=org_id))
        activity_list = list(Activity.query.filter_by(organization_id=org_id))
        for class_ in class_list:
            class_dict = {
                'id': class_.id,
                'name': class_.name,
                'age': class_.age.age,
                'price': class_.price,
                'start_time': class_.start_time,
                'end_time': class_.end_time
            }
            data['classes'].append(class_dict)
        for activity in activity_list:
            activity_dict = {
                'id': activity.id,
                'name': activity.name,
                'age': activity.age.age,
                'price': activity.price,
                'start_time': activity.start_time,
                'end_time': activity.end_time
            }
            data['activities'].append(activity_dict)
    else:
        data[STATUS] = ORGANIZATION_NOT_EXISTS
    return json.dumps(data)