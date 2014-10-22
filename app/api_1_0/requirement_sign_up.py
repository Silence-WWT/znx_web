# -*- coding: utf-8 -*-
import json
from datetime import datetime

from flask import request

from app import db
from ..models import Register, Location
from . import api
from api_constants import *


@api.route('/register_requirement')
def register_requirement():
    data = {}
    name = request.args.get('name')
    cellphone = request.args.get('cellphone')
    need = request.args.get('need')
    city = request.args.get('city')
    district = request.args.get('district')
    location = Location.query.filter(city=city, district=district).first()
    timestamp = datetime.now()
    if name and cellphone and need and location:
        register = Register(
            name=name,
            cellphone=cellphone,
            need=need,
            location=location.id,
            timestamp=timestamp
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