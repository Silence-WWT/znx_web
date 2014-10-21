# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import Organization, OrganizationComment, Class, Activity, Location, Age
from . import api
from api_constants import *


@api.route('/organization_detail')
def organization_detail():
    data = {}
    org_id = request.args.get('organization')
    organization = Organization.query.filter_by(id=org_id).first()
    if organization:
        data = {STATUS: SUCCESS, 'classes': [], 'activities': []}
        location = Location.query.filter_by(id=organization.location).first()
        comments_count = OrganizationComment.query.filter_by(organization_id=organization.id).count()
        org_dict = {
            'id': organization.id,
            'name': organization.name,
            'photo': organization.photo,
            'location': location.district,
            'intro': organization.intro,
            'address': organization.address,
            'cellphone': organization.cellphone,
            'comments_count': comments_count
        }
        data['organization'] = org_dict
        class_list = Class.query.filter_by(organization_id=org_id)
        activity_list = Activity.query.filter_by(organization_id=org_id)
        for class_ in class_list:
            age = Age.query.filter_by(id=class_.age_id).first()
            class_dict = {
                'id': class_.id,
                'name': class_.name,
                'age': age.age,
                'price': class_.price,
                'start_time': str(class_.start_time),
                'end_time': str(class_.end_time)
            }
            data['classes'].append(class_dict)
        for activity in activity_list:
            age = Age.query.filter_by(id=activity.age_id).first()
            activity_dict = {
                'id': activity.id,
                'name': activity.name,
                'age': age.age,
                'price': activity.price,
                'start_time': str(activity.start_time),
                'end_time': str(activity.end_time)
            }
            data['activities'].append(activity_dict)
    else:
        data[STATUS] = ORGANIZATION_NOT_EXISTS
    return json.dumps(data)