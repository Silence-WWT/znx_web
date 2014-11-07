# -*- coding: utf-8 -*-
import json
import math
import time

from flask import request

from app import db
from ..models import User, Organization, OrganizationProfession, OrganizationComment, Type, Profession, Location, City
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
    org_type = request.args.get('type', u'机构', type=unicode)
    type_ = Type.query.filter_by(type=org_type).first()
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
    elif type_:
        org_query = Organization.query.filter_by(type_id=type_.id)
    else:
        data['status'] = TYPE_NOT_EXIST
        return json.dumps(data)
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
            organization_profession_list = OrganizationProfession.query.filter_by(profession_id=profession.id)
            organization_id_list = [org_profession.organization_id for org_profession in organization_profession_list]
            org_list = org_query.filter(Organization.id.in_(organization_id_list),
                                        Organization.location_id.in_(location_id_list))\
                .paginate(page, PER_PAGE, False).items
        else:
            data['status'] = PROFESSION_NOT_EXIST
            return json.dumps(data)
    else:
        org_list = org_query.paginate(page, PER_PAGE, False).items
    for org in org_list:
        location = Location.query.get(org.location_id)
        city = City.query.get(location.city_id)
        org_dict = {
            'id': org.id,
            'name': org.name,
            'city': city.city,
            'district': location.district,
            'photo': '',
            'intro': org.detail,
        }
        if distance:
            delta_latitude = math.fabs(latitude - org.latitude)
            delta_longitude = math.fabs(longitude - org.longitude)
            delta_x = delta_latitude * EARTH_CIRCUMFERENCE / 360
            delta_y = delta_longitude * (EARTH_CIRCUMFERENCE * math.sin(math.radians(90 - latitude))) / 360
            org_dict['distance'] = math.sqrt(delta_x ** 2 + delta_y ** 2)
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
        comments_count = organization.get_comment_count()
        if comments_count:
            start_count = sum([comment.stars for comment in organization.get_comments()])
            stars = float(start_count) / comments_count
        else:
            stars = 0
        org_dict = {
            'id': organization.id,
            'name': organization.name,
            'photo': organization.photo,
            'logo': organization.logo,
            'city': city.city,
            'district': location.district,
            'intro': organization.detail,
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
    comment = request.values.get('comment', u'', type=unicode)
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
            created=time.time()
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


@api.route('/organization_search')
def organization_search():
    data = {'organizations': []}
    name = request.values.get('name', u'', type=unicode)
    organization_list = Organization.query.filter(Organization.name.like(u'%' + name + u'%')).all()
    for organization in organization_list:
        location = Location.query.get(organization.location_id)
        city = City.query.get(location.city_id)
        data['organizations'].append({
            'id': organization.id,
            'name': organization.name,
            'city': city.city,
            'district': location.district,
            'photo': '',
            'intro': organization.detail,
        })
    data['status'] = SUCCESS
    return json.dumps(data)