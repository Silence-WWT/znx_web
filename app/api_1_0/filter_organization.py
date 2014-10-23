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
    city = request.args.get('city')
    district = request.args.get('district')
    profession = request.args.get('profession')
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

    if city and district:
        location = Location.query.filter_by(city=city, district=district).frist()
        if location:
            org_list = org_query.filter_by(location=location.id).paginate(page, PER_PAGE, False).items
        else:
            data['status'] = CITY_NOT_EXIST
            return json.dumps(data)
    elif profession:
        profession = Profession.query.filter_by(profession=profession).first()
        if profession:
            org_list = org_query.filter_by(profession=profession.id).paginate(page, PER_PAGE, False).items
        else:
            data['status'] = PROFESSION_NOT_EXIST
            return json.dumps(data)
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