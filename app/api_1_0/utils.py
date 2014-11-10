# -*- coding: utf-8 -*-
import math

from app import db
from app.models import *
from api_constants import *


def get_ages(obj):
    if isinstance(obj, Organization):
        query = OrganizationAge.query.filter_by(organization_id=obj.id).all()
    elif isinstance(obj, Class):
        query = ClassAge.query.filter_by(class_id=obj.id).all()
    elif isinstance(obj, Activity):
        query = ActivityAge.query.filter_by(activity_id=obj.id).all()
    else:
        query = []
    age_list = []
    for item in query:
        age = Age.query.get(item.age_id)
        age_list.append(age.age)
    return age_list


def get_professions(obj):
    profession_list = []
    if isinstance(obj, Organization):
        query = OrganizationProfession.query.filter_by(organization_id=obj.id)
        for item in query:
            profession = Profession.query.get(item.profession_id)
            profession_list.append(profession.profession)
    return profession_list


def get_unified(user_id, mobile_key):
    unified = UnifiedId.query.filter_by(mobile_key=mobile_key).first()
    if not unified and user_id:
        unified = UnifiedId.query.filter_by(user_id=user_id).first()
    if not unified:
        unified = UnifiedId(
            user_id=user_id,
            mobile_key=mobile_key,
            web_key='',
            created=time.time()
        )
        db.session.add(unified)
        db.session.commit()
    return unified


def organization_filter_by_distance(distance, longitude, latitude):
    delta_latitude = distance / EARTH_CIRCUMFERENCE * 360
    delta_longitude = distance / (EARTH_CIRCUMFERENCE * math.sin(math.radians(90 - latitude))) * 360
    org_query = Organization.query.filter(Organization.latitude <= latitude + delta_latitude,
                                          Organization.latitude >= latitude - delta_latitude,
                                          Organization.longitude <= longitude + delta_longitude,
                                          Organization.longitude >= longitude - delta_longitude)
    return org_query


def get_organization_distance(longitude, latitude, org_longitude, org_latitude):
    delta_latitude = math.fabs(latitude - org_latitude)
    delta_longitude = math.fabs(longitude - org_longitude)
    delta_x = delta_latitude * EARTH_CIRCUMFERENCE / 360
    delta_y = delta_longitude * (EARTH_CIRCUMFERENCE * math.sin(math.radians(90 - latitude))) / 360
    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
    return distance