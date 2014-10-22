# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import Organization, Profession, Location
from . import api
from api_constants import *


@api.route('/get_location_profession')
def get_location_profession():
    data = {'districts': [], 'professions': []}
    city = request.args.get('city')
    if city:
        location_list = Location.query.filter_by(city=city)
        districts = [location.district for location in location_list]
        location_id_list = [location.id for location in location_list]
        organization_list = Organization.query.filter(Organization.location.in_(location_id_list))\
            .group_by(Organization.profession)
        profession_id_list = [organization.profession for organization in organization_list]
        profession_list = Profession.query.filter(Profession.id.in_(profession_id_list))
        professions = [profession.profession for profession in profession_list]
        data['status'] = SUCCESS
        data['districts'] = districts
        data['professions'] = professions
    else:
        data['status'] = PARAMETER_ERROR
    return json.dumps(data)