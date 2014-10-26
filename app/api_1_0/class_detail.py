# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import Class, ClassComment, Age
from . import api
from api_constants import *


@api.route('/class_detail')
def class_detail():
    data = {'class': {}}
    class_id = request.args.get('class')
    class_ = Class.query.filter_by(id=class_id).first()
    if class_:
        age = Age.query.filter_by(id=class_.age_id).first()
        comments_count = ClassComment.query.filter_by(class_id=class_.id).count()
        data['class'] = {
            'id': class_.id,
            'name': class_.name,
            'age': age.age,
            'price': class_.price,
            'intro': class_.intro,
            'consult_time': class_.consult_time,
            'is_round': class_.is_round,
            'is_tastable': class_.is_tastable,
            'comments_count': comments_count,
            'days': class_.days
        }
        data['status'] = SUCCESS
    else:
        data['status'] = CLASS_NOT_EXIST
    return json.dumps(data)