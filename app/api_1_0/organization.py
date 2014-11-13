# -*- coding: utf-8 -*-
import json
import time

from flask import request

from app import db
from ..models import User, Organization, OrganizationProfession, OrganizationComment, Type, Profession, Location, City
from . import api
from api_constants import *
from utils import organization_filter_by_distance, get_organization_distance, cmp_distance, paginate


@api.route('/organization_filter')
def organization_filter():
    data = {'organizations': []}
    page = request.values.get('page', 1, type=int)
    city = request.values.get('city', u'', type=unicode)
    district = request.values.get('district', u'', type=unicode)
    profession = request.values.get('profession', u'', type=unicode)
    distance = request.values.get('distance', 0.0, type=float)
    org_type = request.values.get('type', u'机构', type=unicode)
    name = request.values.get('name', u'', type=unicode)
    type_ = Type.query.filter_by(type=org_type).limit(1).first()
    city = City.query.filter_by(city=city).limit(1).first()

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

    if name:
        org_query = org_query.filter(Organization.name.like(u'%' + name + u'%'))

    if city and district and district != u'all' and not distance and not name:
        location = Location.query.filter_by(city_id=city.id, district=district).limit(1).first()
        if location:
            org_query = org_query.filter_by(location_id=location.id)
        else:
            data['status'] = CITY_NOT_EXIST
            return json.dumps(data)

    if profession and profession != u'all' and not name:
        profession = Profession.query.filter_by(profession=profession).limit(1).first()
        if profession:
            location_list = Location.query.filter_by(city_id=city.id)
            location_id_list = [location.id for location in location_list]
            organization_profession_list = OrganizationProfession.query.filter_by(profession_id=profession.id)
            organization_id_list = [org_profession.organization_id for org_profession in organization_profession_list]
            org_query = org_query.filter(Organization.id.in_(organization_id_list),
                                         Organization.location_id.in_(location_id_list))
        else:
            data['status'] = PROFESSION_NOT_EXIST
            return json.dumps(data)

    if city and (district == u'all' or profession == u'all'):
        location_query = Location.query.filter_by(city_id=city.id)
        org_query = org_query.filter(Organization.location_id.in_([location.id for location in location_query]))

    if distance:
        cmp_list = [(org, longitude, latitude) for org in org_query]
        org_list = paginate(sorted(cmp_list, cmp=cmp_distance), page)
        org_list = [org[0] for org in org_list]
    else:
        org_list = org_query.paginate(page, PER_PAGE, False).items

    for org in org_list:
        org.page_view_inc()
        location = Location.query.get(org.location_id)
        city = City.query.get(location.city_id) if location else None
        org_dict = {
            'id': org.id,
            'name': org.name,
            'city': city.city if city else '',
            'district': location.district if location else '',
            'photo': STATIC_URL + org.photo if org.photo else '',
            'logo': STATIC_URL + org.logo if org.logo else '',
            'intro': org.detail
        }
        if distance:
            org_dict['distance'] = get_organization_distance(longitude, latitude, org.longitude, org.latitude)
            if org_dict['distance'] <= distance:
                data['organizations'].append(org_dict)
        else:
            data['organizations'].append(org_dict)
    data['status'] = SUCCESS
    return json.dumps(data)


@api.route('/organization_detail')
def organization_detail():
    data = {}
    organization_id = request.args.get('organization')
    organization = Organization.query.get(organization_id)
    if organization:
        data['status'] = SUCCESS
        location = Location.query.get(organization.location_id)
        city = City.query.get(location.city_id) if location else None
        organization.page_view_inc()
        org_dict = {
            'id': organization.id,
            'name': organization.name,
            'photo': STATIC_URL + organization.photo if organization.photo else '',
            'logo': STATIC_URL + organization.logo,
            'city': city.city if city else '',
            'district': location.district if location else '',
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
    user = User.query.get(user_id)
    organization = Organization.query.get(organization_id)
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
    organization = Organization.query.get(organization_id)
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
    organization_list = org_query.filter(Organization.name.like(u'%' + name + u'%'))
    if distance:
        cmp_list = [(org, longitude, latitude) for org in organization_list]
        organization_list = paginate(sorted(cmp_list, cmp=cmp_distance), page)
        organization_list = [org[0] for org in organization_list]
    else:
        organization_list = organization_list.paginate(page, PER_PAGE, False).items

    for organization in organization_list:
        location = Location.query.get(organization.location_id)
        city = City.query.get(location.city_id) if location else None
        org_dict = {
            'id': organization.id,
            'name': organization.name,
            'city': city.city if city else '',
            'district': location.district if location else '',
            'photo': STATIC_URL + organization.photo if organization.photo else '',
            'logo': STATIC_URL + organization.logo if organization.logo else '',
            'intro': organization.detail
        }
        if distance:
            org_dict['distance'] = get_organization_distance(longitude, latitude,
                                                             organization.longitude, organization.latitude)
            if org_dict['distance'] <= distance:
                data['organizations'].append(org_dict)
        else:
            data['organizations'].append(org_dict)
    data['status'] = SUCCESS
    return json.dumps(data)