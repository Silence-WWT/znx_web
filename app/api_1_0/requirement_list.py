# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import Register
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
    return json.dumps(data)