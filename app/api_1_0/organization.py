# -*- coding: utf-8 -*-
import json
import math
from time import time as time_now

from flask import request

from app import db
from ..models import User, Organization, OrganizationComment, Profession, Location, City
from . import api
from api_constants import *


@api.route('/organization_filter')
def organization_filter():
    data = {'organizations': []}
    page = request.values.get('page', 1, type=int)
    city = request.args.get('city', '').encode('utf8')
    district = request.args.get('district', '').encode('utf8')
    profession = request.args.get('profession', '').encode('utf8')
    distance = request.values.get('distance', 0.0, type=float)
    city = City.query.filter_by(city=city).first()
    if distance:
        latitude = request.values.get('latitude', 0.0, type=float)
        longitude = request.values.get('longitude', 0.0, type=float)
        if latitude and longitude:
            delta_latitude = distance / EARTH_CIRCUMFERENCE * 360
            delta_longitude = distance / (EARTH_CIRCUMFERENCE * math.sin(math.radians(90 - latitude))) * 360
            org_query = Organization.query.filter(Organization.latitude <= latitude + delta_latitude,
                                                  Organization.latitude >= latitude - delta_latitude,
                                                  Organization.longitude <= longitude + delta_longitude,
                                                  Organization.longitude >= longitude - delta_longitude)
        else:
            data['status'] = PARAMETER_ERROR
            return json.dumps(data)
    else:
        org_query = Organization.query
    if city and district:
        location = Location.query.filter_by(city_id=city.id, district=district).first()
        if location:
            org_list = org_query.filter_by(location_id=location.id).paginate(page, PER_PAGE, False).items
        else:
            data['status'] = CITY_NOT_EXIST
            return json.dumps(data)
    elif city and profession:
        profession = Profession.query.filter_by(profession=profession).first()
        if profession:
            location_list = Location.query.filter_by(city_id=city.id)
            location_id_list = [location.id for location in location_list]
            org_list = org_query.filter(Organization.profession_id == profession.id,
                                        Organization.location_id.in_(location_id_list))\
                .paginate(page, PER_PAGE, False).items
        else:
            data['status'] = PROFESSION_NOT_EXIST
            return json.dumps(data)
    else:
        data['status'] = PARAMETER_ERROR
        return json.dumps(data)
    for org in org_list:
        location = Location.query.get(org.location_id)
        city = City.query.get(location.city_id)
        org_dict = {
            'id': org.id,
            'name': org.name,
            'city': city.city,
            'district': location.district,
            'photo': '',
            'intro': org.intro,
        }
        if distance:
            delta_latitude = math.fabs(latitude - org.latitude)
            delta_longitude = math.fabs(longitude - org.longitude)
            delta_x = delta_latitude * EARTH_CIRCUMFERENCE / 360
            delta_y = delta_longitude * (EARTH_CIRCUMFERENCE * math.sin(math.radians(90 - latitude))) / 360
            org_dict['distance'] = math.sqrt(delta_x**2 + delta_y**2)
        data['organizations'].append(org_dict)
    if distance:
        data['organizations'].sort(key=lambda x: x['distance'])
    data['status'] = SUCCESS
    return json.dumps(data)


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


@api.route('/organization_comment')
def organization_comment():
    data = {}
    user_id = request.args.get('user_id')
    comment = request.args.get('comment', '').encode('utf8')
    organization_id = request.args.get('organization')
    stars = request.values.get('stars', 0, type=int)
    user = User.query.filter_by(id=user_id).first()
    organization = Organization.query.filter_by(id=organization_id).first()
    if user and organization and 1 <= stars <= 5:
        org_comment = OrganizationComment(
            organization_id=organization.id,
            user_id=user.id,
            stars=stars,
            body=comment,
            created=time_now()
        )
        db.session.add(org_comment)
        db.session.commit()
        data['status'] = SUCCESS
    elif not organization:
        data['status'] = ORGANIZATION_NOT_EXIST
    elif not user:
        data['status'] = USER_NOT_EXIST
    else:
        data['status'] = PARAMETER_ERROR
    return json.dumps(data)


@api.route('/organization_comment_list')
def organization_comment_list():
    data = {'organization_comments': []}
    page = request.values.get('page', 1, type=int)
    organization_id = request.args.get('organization')
    organization = Organization.query.filter_by(id=organization_id).first()
    if organization:
        comment_list = OrganizationComment.query.filter_by(organization_id=organization_id).\
            order_by(-OrganizationComment.created).\
            paginate(page, PER_PAGE, False).items
        for comment in comment_list:
            user = User.query.get(comment.user_id)
            comment_dict = {
                'body': comment.body,
                'stars': comment.stars,
                'created': comment.created,
                'username': user.username
            }
            data['organization_comments'].append(comment_dict)
        data['status'] = SUCCESS
    else:
        data['status'] = ORGANIZATION_NOT_EXIST
    return json.dumps(data)