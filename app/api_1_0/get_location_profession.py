# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import Organization, Profession, Location, City
from . import api
from api_constants import *
from helper import get_professions


@api.route('/get_district_profession')
def get_district_profession():
    data = {'districts': [], 'professions': []}
    city = City.query.filter_by(city=request.args.get('city', '').encode('utf8')).first()
    if city:
        location_list = Location.query.filter_by(city_id=city.id)
        districts = [location.district for location in location_list]
        location_id_list = [location.id for location in location_list]
        organization_list = Organization.query.filter(Organization.location_id.in_(location_id_list))
        profession_set = set()
        for organization in organization_list:
            for profession in get_professions(organization):
                profession_set.add(profession)
        professions = list(profession_set)
        data['status'] = SUCCESS
        data['districts'] = districts
        data['professions'] = professions
    else:
        data['status'] = PARAMETER_ERROR
    return json.dumps(data)