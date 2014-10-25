# -*- coding: utf-8 -*-
from flask import Blueprint

course = Blueprint('course', __name__)
from . import views

