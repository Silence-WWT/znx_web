# -*- coding: utf-8 -*-
import json
from time import time as time_now

from flask import request

from app import db
from ..models import User, Organization, OrganizationComment
from . import api
from api_constants import *


@api.route('/organization_comment')
def organization_comment():
    data = {}
    username = request.args.get('username')
    organization_id = request.args.get('organization')
    comment = request.args.get('comment')
    stars = request.args.get('stars')
    user = User.query.filter_by(username=username).first()
    organization = Organization.query.filter_by(id=organization_id).first()
    if user and organization and comment and u'1' <= stars <= u'5' and len(stars) == 1:
        org_comment = OrganizationComment(
            organization_id=organization.id,
            user_id=user.id,
            stars=stars,
            body=comment,
            created=time_now()
        )
        try:
            db.session.add(org_comment)
            db.session.commit()
        except Exception:
            data['status'] = SQL_EXCEPTION
        else:
            data['status'] = SUCCESS
    elif not organization:
        data['status'] = ORGANIZATION_NOT_EXIST
    else:
        data['status'] = PARAMETER_ERROR
    return json.dumps(data)