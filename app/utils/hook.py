# -*- coding: utf-8 -*-
from flask import session
from ..models import City

def city_session():
    if 'city_id' not in session:
        session['city_id'] = 1

def cities():
    return dict(cities=City.query.all())

