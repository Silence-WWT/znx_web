# -*- coding: utf-8 -*-
import time
from .models import Category, City


def stars(num):
    num = int(num)
    if num <=5:
        return '<i class="level_solid"></i>'*num + \
               '<i class="level_hollow"></i>'*(5-num)
    else:
        return stars(num/10)


def category(category_id):
    category = Category.query.get(category_id)
    return category.category


def city(city_id):
    city=City.query.get(city_id)
    return city.city

def sex(s):
    if s:
        return u'男'
    else:
        return u'女'


def get_date_time(timestamp):
    return time.strftime('%Y-%m-%d %H:%M', time.localtime(timestamp))


def anonymous_name(name):
    return name[0]+u'同学'


def anonymous_mobile(mobile):
    return mobile[0:3]+'xxxxx'+ mobile[-3:]
