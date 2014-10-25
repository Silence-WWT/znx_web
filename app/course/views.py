# -*- coding: utf-8 -*-
from . import course
from ..models import Class
from flask import render_template
@course.route('/home/<int:id>')
def home(id):
    course = Class.query.get_or_404(id)
    return render_template('organclass_py.html', course=course)

