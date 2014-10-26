# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import Organization, OrganizationComment, Location, City
from . import api
from api_constants import *


@api.route('/organization_detail')
def organization_detail():
    data = {}
    organization_id = request.args.get('organization')
    organization = Organization.query.filter_by(id=organization_id).first()
    if organization:
        data['status'] = SUCCESS
        location = Location.query.get(organization.location_id)
        city = City.query.get(location.city_id)
        org_comment_query = OrganizationComment.query.filter_by(organization_id=organization.id)
        comments_count = org_comment_query.count()
        start_count = sum([comment.stars for comment in org_comment_query])
        stars = float(start_count) / comments_count
        org_dict = {
            'id': organization.id,
            'name': organization.name,
            'photo': organization.photo,
            'logo': organization.logo,
            'city': city.city,
            'district': location.district,
            'intro': organization.intro,
            'address': organization.address,
            'mobile': organization.mobile,
            'comments_count': comments_count,
            'stars': stars,
            'traffic': organization.traffic
        }
        data['organization'] = org_dict
    else:
        data['status'] = ORGANIZATION_NOT_EXIST
    return json.dumps(data)