# -*- coding: utf-8 -*-
import json

from flask import request

from ..models import User
from . import api
from api_constants import *


@api.route('/confirm_cellphone')
def confirm_cellphone():
    data = {}
    cellphone = request.args.get('cellphone')
    if User.query.filter_by(cellphone=cellphone).first():
        data[STATUS] = CELLPHONE_EXISTS
    else:
        data[STATUS] = SUCCESS
    return json.dumps(data)