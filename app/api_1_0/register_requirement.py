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
    method = None
    try:
        method = int(request.args.get('method'))
    except Exception:
        data['status'] = PARAMETER_ERROR
    if method == GET:
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
                data['status'] = PARAMETER_ERROR
            data['status'] = SUCCESS
        else:
            data['status'] = PARAMETER_ERROR
    elif method == POST:
        try:
            page = int(request.args.get('page'))
        except Exception:
            page = 1
        data['registers'] = []
        register_list = Register.query.all().paginate(page, PER_PAGE, False)
        for register in register_list:
            if len(register.name) == 2 or len(register.name) == 3:
                last_name = register.name[:1]
            else:
                last_name = register.name[:2]
            cellphone = register.cellphone[:3]
            register_dict = {
                'name': last_name + u'同学',
                'cellphone': cellphone + '*' * 8,
                'need': register.need,
                'time': str(register.timestamp)
            }
            data['registers'].append(register_dict)
        data['status'] = SUCCESS
    else:
        data['status'] = PARAMETER_ERROR
    return json.dumps(data)