# -*- coding: utf-8 -*-
import json

from ..models import City, Organization, Location
from . import api
from api_constants import *


@api.route('/get_cities')
def get_cities():
    data = {'status': SUCCESS}
    org_list = Organization.query.group_by(Organization.location_id).all()
    location_list = Location.query.filter(Location.id.in_([org.location_id for org in org_list])).\
        group_by(Location.city_id).all()
    city_list = City.query.filter(City.id.in_([location.city_id for location in location_list]))
    data['cities'] = [city.city for city in city_list]
    return json.dumps(data)