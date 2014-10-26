# -*- coding: utf-8 -*-
from flask import Blueprint

api = Blueprint('api', __name__)

from .import user
from .import organization
from .import class_
from .import activity
from .import order
from .import requirement
from .import get_location_profession