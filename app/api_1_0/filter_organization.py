import json
import re

from flask import request

from ..models import Organization
from . import api
from api_constants import *


@api.route('/filter_organization')
def filter_organization():
    # TODO: update after completed models
    data = {'organizations': []}
    org_list = []
    if request.args.get('location'):
        location_list = re.findall('location=(\w+?)', request.query_string)
        for location in location_list:
            org_list.extend(list(Organization.query.filter_by(location=location)))
    elif request.args.get('property'):
        property_list = re.findall('property=(\w+?)', request.query_string)
        for property_ in property_list:
            org_list.extend(list(Organization.query.filter_by(property=property_)))
    elif request.args.get('condition'):
        condition = re.match('condition=(\w+?)', request.query_string).group(1)
        if condition == COMMENTS_COUNT:
            org_list.extend(list(Organization.query.order_by(Organization.comments.count()).limit(20).all()))
        elif condition == SKIM_COUNT:
            org_list.extend(list(Organization.query.order_by(Organization.skims.count()).limit(20).all()))
        elif condition == ORDER_COUNT:
            org_list.extend(list(Organization.query.order_by(Organization.orders.count()).limit(20).all()))
    for org in org_list:
        org_dict = {
            'id': org.id,
            'name': org.name,
            'location': org.location,
            'photo': org.photo.url,
            'intro': org.intro
        }
        data['organizations'].append(org_dict)
    data[STATUS] = SUCCESS
    return json.dumps(data)