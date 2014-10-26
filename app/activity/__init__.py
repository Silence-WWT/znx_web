# -*- coding: utf-8 -*-
from flask import Blueprint

activity = Blueprint('activity', __name__)
from . import views

