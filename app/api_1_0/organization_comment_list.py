# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import Organization, OrganizationComment
from . import api
from api_constants import *


@api.route('/organization_comment_list')
def organization_comment_list():
    data = {'organization_comments': []}
    try:
        page = int(request.args.get('page'))
    except TypeError:
        page = 1
    except ValueError:
        data['status'] = PARAMETER_ERROR
        return json.dumps(data)
    organization_id = request.args.get('organization')
    organization = Organization.query.filter_by(id=organization_id).first()
    if organization:
        comment_list = OrganizationComment.query.filter_by(organization_id=organization_id).paginate(page, PER_PAGE, False).items
        for comment in comment_list:
            comment_dict = {
                'body': comment.body,
                'stars': comment.stars,
                'timestamp': str(comment.timestamp)
            }
            data['organization_comments'].append(comment_dict)
        data['status'] = SUCCESS
    else:
        data['status'] = ORGANIZATION_NOT_EXIST
    return json.dumps(data)