# -*- coding: utf-8 -*-
import json

from ..models import City
from . import api
from api_constants import *


@api.route('/get_cities')
def get_cities():
    data = {'status': SUCCESS, 'cities': []}
    city_list = City.query.all()
    for city in city_list:
        data['cities'].append(city.city)
    return json.dumps(data)