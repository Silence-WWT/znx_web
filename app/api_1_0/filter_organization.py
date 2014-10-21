# -*- coding: utf-8 -*-
import json
import math

from flask import request
from sqlalchemy.sql import func, desc

from app import db
from ..models import Organization, OrganizationComment, Class, ClassOrder, Activity, ActivityOrder, Location
from . import api
from . import helper
from api_constants import *


@api.route('/filter_organization')
def filter_organization():
    data = {'organizations': []}
    org_list = []
    sort_key = ''
    result_dict = {}
    try:
        page = int(request.args.get('page'))
    except TypeError:
        page = 1
    city_list = request.args.getlist('city')
    district_list = request.args.getlist('district')
    property_list = request.args.getlist('property')
    condition = request.args.get('condition')
    distance = request.args.get('distance')
    if distance:
        try:
            distance = float(distance)
            latitude = float(request.args.get('latitude'))
            longitude = float(request.args.get('longitude'))
            delta_latitude = distance / EARTH_CIRCUMFERENCE * 360
            delta_longitude = distance / (EARTH_CIRCUMFERENCE * math.sin(90 - latitude)) * 360
            org_query = Organization.query.filter(Organization.latitude <= latitude + delta_latitude,
                                                  Organization.latitude >= latitude - delta_latitude,
                                                  Organization.longitude <= longitude + delta_longitude,
                                                  Organization.longitude >= longitude - delta_longitude)
            print(org_query)
            print(org_query.all())
        except TypeError:
            data['status'] = PARAMETER_ERROR
            return json.dumps(data)
    else:
        org_query = Organization.query

    if city_list and len(city_list) == len(district_list):
        city_district_list = map(lambda city, district: (city, district), city_list, district_list)
        location_list = []
        for (city, district) in city_district_list:
            location = Location.query.filter_by(city=city, district=district).frist()
            if location:
                location_list.append(location.id)
        org_list = org_query.filter(Organization.location.in_(location_list)) \
            .paginate(page, PER_PAGE, False).items

    elif property_list:
        property_list = request.args.getlist('property')
        org_list = org_query.filter(Organization.property_.in_(property_list)) \
            .paginate(page, PER_PAGE, False).items

    elif condition:
        try:
            condition = int(condition)
        except TypeError:
            data['status'] = PARAMETER_ERROR
            return json.dumps(data)
        if condition == VIEW_COUNT:
            sort_key = 'view_count'
            org_list = org_query.order_by(-Organization.page_view) \
                .paginate(page, PER_PAGE, False).items

        elif condition == COMMENTS_COUNT:
            sort_key = 'comments_count'
            if distance:
                org_id_list = [org.id for org in org_query.all()]
                org_condition_list = db.session.query(OrganizationComment.organization_id,
                                                      func.count('*').label('comments_count'))\
                    .filter(OrganizationComment.organization_id.in_(org_id_list))\
                    .group_by(OrganizationComment.organization_id)\
                    .order_by(desc('comments_count'))
            else:
                org_condition_list = db.session.query(OrganizationComment.organization_id,
                                                      func.count('*').label('comments_count'))\
                    .group_by(OrganizationComment.organization_id)\
                    .order_by(desc('comments_count'))

        elif condition == ORDER_COUNT:
            sort_key = 'orders_count'
            class_order_query_result = db.session.query(ClassOrder.class_id,
                                                        func.count('*').label('class_orders_count')) \
                .group_by(ClassOrder.class_id) \
                .order_by(desc('class_orders_count'))
            activity_order_query_result = db.session.query(ActivityOrder.activity_id,
                                                           func.count('*').label('activity_orders_count')) \
                .group_by(ActivityOrder.activity_id) \
                .order_by(desc('activity_orders_count'))
            class_org_query_result = db.session.query(Class.id, Class.organization_id)
            activity_org_query_result = db.session.query(Activity.id, Activity.organization_id)
            class_org_dict = {result[0]: result[1] for result in class_org_query_result}
            activity_org_dict = {result[0]: result[1] for result in activity_org_query_result}
            org_orders_count_dict = {org.id: [] for org in org_query.all()}

            for class_ in class_order_query_result:
                org_id = class_org_dict[class_[0]]
                if org_id in org_orders_count_dict:
                    orders_count = class_[1]
                    org_orders_count_dict[org_id].append(orders_count)
            for activity in activity_order_query_result:
                org_id = activity_org_dict[activity[0]]
                if org_id in org_orders_count_dict:
                    orders_count = activity[1]
                    org_orders_count_dict[org_id].append(orders_count)
            org_orders_count_list = [(org, sum(count_list)) for org, count_list in org_orders_count_dict.items()]
            org_condition_list = sorted(org_orders_count_list, key=lambda x: x[1], reverse=True)
        else:
            data['status'] = PARAMETER_ERROR
            return json.dumps(data)
        if condition == COMMENTS_COUNT or condition == ORDER_COUNT:
            result_list = helper.paginate([result for result in org_condition_list], page, PER_PAGE)
            result_dict = {result[0]: result[1] for result in result_list}
            org_list = org_query.filter(Organization.id.in_([result[0] for result in result_list]))
            print(len(result_list), org_list.count())
    else:
        data['status'] = PARAMETER_ERROR
        return json.dumps(data)
    for org in org_list:
        location = Location.query.filter_by(id=org.location).first()
        org_dict = {
            'id': org.id,
            'name': org.name,
            'city': location.city,
            'district': location.district,
            'photo': org.photo,
            'intro': org.intro,
        }
        if sort_key and condition == VIEW_COUNT:
            org_dict[sort_key] = org.page_view
        elif sort_key:
            org_dict[sort_key] = result_dict[org.id]
        data['organizations'].append(org_dict)
    if sort_key and condition != VIEW_COUNT:
        data['organizations'] = sorted(data['organizations'], key=lambda x: x[sort_key], reverse=True)
    data['status'] = SUCCESS
    return json.dumps(data)