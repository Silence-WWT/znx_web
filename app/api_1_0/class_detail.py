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
            'start_time': str(class_.start_time),
            'end_time': str(class_.end_time),
            'try': class_.try_,
            'comments_count': comments_count,
            'course_count': ''  # 总课时，等待数据库更新
        }
        data['status'] = SUCCESS
    else:
        data['status'] = CLASS_NOT_EXIST
    return json.dumps(data)