# -*- coding: utf-8 -*-
import json

from ..models import City
from . import api
from api_constants import *


@api.route('/get_cities')
def get_cities():
    data = {'status': SUCCESS}
    city_list = City.query.all()
    data['cities'] = [city.city for city in city_list]
    return json.dumps(data)