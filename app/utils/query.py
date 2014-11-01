# -*- coding: utf-8 -*-
from ..models import Location, City
from wtforms.widgets import html_params


def get_location():
    locations = Location.query.all()
    location_dict = dict()
    for location in locations:
        city = City.query.get(location.city_id).city
        if city not in location_dict.keys():
            location_dict[city] = set()
        location_dict[city].add((location.id, location.district))
    return location_dict


def select_multi_checkbox(field, ul_class='', **kwargs):
    kwargs.setdefault('type', 'checkbox')
    field_id = kwargs.pop('id', field.id)
    html = [u'<ul %s>' % html_params(id=field_id, class_=ul_class)]
    for value, label, checked in field.iter_choices():
        choice_id = u'%s-%s' % (field_id, value)
        options = dict(kwargs, name=field.name, value=value, id=choice_id)
        if checked:
            options['checked'] = 'checked'
        html.append(u'<label class="checkbox inline">')
        html.append(u'<input %s class="class_time" /> %s </label>' % (html_params(**options), label))
    return u''.join(html)
