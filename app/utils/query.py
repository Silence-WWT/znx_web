# -*- coding: utf-8 -*-
from ..models import Location, City


def get_location():
    locations = Location.query.all()
    location_dict = dict()
    for location in locations:
        city = City.query.get(location.city_id).city
        if city not in location_dict.keys():
            location_dict[city] = set()
        location_dict[city].add((location.id, location.district))
    return location_dict

