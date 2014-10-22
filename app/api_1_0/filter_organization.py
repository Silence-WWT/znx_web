# -*- coding: utf-8 -*-
import json
import math

from flask import request

from ..models import Organization, Profession, Location
from . import api
from api_constants import *


@api.route('/filter_organization')
def filter_organization():
    data = {'organizations': []}
    try:
        page = int(request.args.get('page'))
    except TypeError:
        page = 1
    except ValueError:
        data['status'] = PARAMETER_ERROR
        return json.dumps(data)
    city_list = request.args.getlist('city')
    district_list = request.args.getlist('district')
    profession_list = request.args.getlist('profession')
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
        except TypeError:
            data['status'] = PARAMETER_ERROR
            return json.dumps(data)
        except ValueError:
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
    elif profession_list:
        professions = Profession.query.filter(Profession.profession.in_(profession_list))
        profession_list = [profession.id for profession in professions]
        org_list = org_query.filter(Organization.profession.in_(profession_list)) \
            .paginate(page, PER_PAGE, False).items
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
        data['organizations'].append(org_dict)
    data['status'] = SUCCESS
    return json.dumps(data)