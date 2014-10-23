# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import Class, ClassComment
from . import api
from api_constants import *


@api.route('/class_comment_list')
def class_comment_list():
    data = {'class_comments': []}
    try:
        page = int(request.args.get('page'))
    except TypeError:
        page = 1
    except ValueError:
        data['status'] = PARAMETER_ERROR
        return json.dumps(data)
    class_id = request.args.get('class')
    class_ = Class.query.filter_by(id=class_id).first()
    if class_:
        comment_list = ClassComment.query.filter_by(class_id=class_id).paginate(page, PER_PAGE, False).items
        for comment in comment_list:
            comment_dict = {
                'body': comment.body,
                'stars': comment.stars,
                'timestamp': str(comment.timestamp)
            }
            data['class_comments'].append(comment_dict)
        data['status'] = SUCCESS
    else:
        data['status'] = CLASS_NOT_EXIST
    return json.dumps(data)