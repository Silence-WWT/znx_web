# -*- coding: utf-8 -*-
import json
from datetime import datetime

from flask import request

from app import db
from ..models import Register, Location, City
from . import api
from api_constants import *


@api.route('/register_requirement')
def register_requirement():
    data = {}
    name = request.args.get('name')
    mobile = request.args.get('mobile')
    need = request.args.get('need')
    city = City.query.filter_by(city=request.args.get('city')).first()
    district = request.args.get('district')
    location = Location.query.filter_by(city_id=city.id, district=district).first()
    created = datetime.now()
    if name and mobile and need and location:
        register = Register(
            name=name,
            mobile=mobile,
            need=need,
            location=location.id,
            created=created
        )
        try:
            db.session.add(register)
            db.session.commit()
        except Exception:
            db.session.rollback()
            data['status'] = SQL_EXCEPTION
        data['status'] = SUCCESS
    else:
        data['status'] = PARAMETER_ERROR
    return json.dumps(data)