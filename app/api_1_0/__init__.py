# -*- coding: utf-8 -*-
from flask import Blueprint

api = Blueprint('api', __name__)

from .import login
from .import register
from .import filter_organization
from .import organization_detail
from .import class_list
from .import class_detail
from .import activity_list
from .import activity_detail
from .import order_list
from .import order_detail
from .import register_requirement