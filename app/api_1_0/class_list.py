# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import Class, Age
from . import api
from api_constants import *


@api.route('/class_list')
def class_list():
    data = {'classes': []}
    try:
        page = int(request.args.get('page'))
    except TypeError:
        page = 1
    except ValueError:
        data['status'] = PARAMETER_ERROR
        return json.dumps(data)
    organization_id = request.args.get('organization')
    class_list_ = Class.query.filter_by(organization_id=organization_id).paginate(page, PER_PAGE, False).items
    for class_ in class_list_:
        age = Age.query.filter_by(id=class_.age_id).first()
        class_dict = {
            'id': class_.id,
            'name': class_.name,
            'age': age.age,
            'price': class_.price,
            'days': class_.days
        }
        data['classes'].append(class_dict)
    data['status'] = SUCCESS
    return json.dumps(data)