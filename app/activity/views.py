# -*- coding: utf-8 -*-
from . import activity
from ..models import Activity
from flask import render_template
@activity.route('/home/<int:id>')
def home(id):
    activity = Activity.query.get_or_404(id)
    return render_template('organact_py.html', activity=activity)

