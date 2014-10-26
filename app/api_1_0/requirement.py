# -*- coding: utf-8 -*-
import json
from time import time as time_now

from flask import request

from app import db
from ..models import Register, City, Location
from . import api
from api_constants import *


@api.route('/requirement_list')
def requirement_list():
    data = {'registers': []}
    try:
        page = int(request.args.get('page'))
    except TypeError:
        page = 1
    except ValueError:
        data['status'] = PARAMETER_ERROR
        return json.dumps(data)
    register_list = Register.query.paginate(page, PER_PAGE, False).items
    for register in register_list:
        if len(register.name) == 2 or len(register.name) == 3:
            last_name = register.name[:1]
        else:
            last_name = register.name[:2]
        mobile = register.mobile[:3]
        register_dict = {
            'name': last_name + u'同学',
            'mobile': mobile + '*' * 8,
            'need': register.need,
            'time': register.created
        }
        data['registers'].append(register_dict)
    data['status'] = SUCCESS
    return json.dumps(data)


@api.route('/requirement_sign_up')
def requirement_sign_up():
    data = {}
    name = request.args.get('name')
    mobile = request.args.get('mobile')
    need = request.args.get('need')
    city = City.query.filter_by(city=request.args.get('city')).first()
    district = request.args.get('district')
    if city:
        location = Location.query.filter_by(city_id=city.id, district=district).first()
    else:
        location = None
    if name and mobile and need and location:
        register = Register(
            name=name,
            mobile=mobile,
            need=need,
            location=location.id,
            created=time_now()
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