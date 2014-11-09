# -*- coding: utf-8 -*-
import json
import time

from flask import request

from app import db
from ..models import User, Organization, OrganizationProfession, OrganizationComment, Type, Profession, Location, City
from . import api
from api_constants import *
from utils import organization_filter_by_distance, get_organization_distance


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
            org_query = organization_filter_by_distance(distance, longitude, latitude)
        else:
            data['status'] = PARAMETER_ERROR
            return json.dumps(data)
    elif type_:
        org_query = Organization.query.filter_by(type_id=type_.id)
    else:
        data['status'] = SUCCESS
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
        org.page_view_inc()
        location = Location.query.get(org.location_id)
        city = City.query.get(location.city_id)
        org_dict = {
            'id': org.id,
            'name': org.name,
            'city': city.city,
            'district': location.district,
            'photo': STATIC_URL + org.photo if org.photo else '',
            'logo': STATIC_URL + org.logo if org.logo else '',
            'intro': org.detail
        }
        if distance:
            org_dict['distance'] = get_organization_distance(longitude, latitude, org.longitude, org.latitude)
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
        organization.page_view_inc()
        org_dict = {
            'id': organization.id,
            'name': organization.name,
            'photo': STATIC_URL + organization.photo if organization.photo else '',
            'logo': STATIC_URL + organization.logo,
            'city': city.city,
            'district': location.district,
            'intro': organization.detail,
            'address': organization.address,
            'mobile': organization.mobile,
            'comments_count': organization.get_comment_count(),
            'stars': organization.star,
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
        organization.set_star(stars)
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
    distance = request.values.get('distance', 0.0, type=float)
    page = request.values.get('page', 1, type=int)
    if distance:
        latitude = request.values.get('latitude', 0.0, type=float)
        longitude = request.values.get('longitude', 0.0, type=float)
        if latitude and longitude:
            org_query = organization_filter_by_distance(distance, longitude, latitude)
        else:
            data['status'] = PARAMETER_ERROR
            return json.dumps(data)
    else:
        org_query = Organization.query
    organization_list = org_query.filter(Organization.name.like(u'%' + name + u'%')).\
        paginate(page, PER_PAGE, False).items
    print(len(organization_list))
    for organization in organization_list:
        location = Location.query.get(organization.location_id)
        city = City.query.get(location.city_id)
        org_dict = {
            'id': organization.id,
            'name': organization.name,
            'city': city.city,
            'district': location.district,
            'photo': STATIC_URL + organization.photo if organization.photo else '',
            'logo': STATIC_URL + organization.logo if organization.logo else '',
            'intro': organization.detail
        }
        if distance:
            org_dict['distance'] = get_organization_distance(longitude, latitude,
                                                             organization.longitude, organization.latitude)
        data['organizations'].append(org_dict)
    data['status'] = SUCCESS
    return json.dumps(data)