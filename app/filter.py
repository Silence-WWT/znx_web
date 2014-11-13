# -*- coding: utf-8 -*-
import time
from .models import Category, City, Type
from flask import current_app


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


def user_or_admin(is_user):
    if is_user:
        return u'用户'
    return u'客服'

def source(source_id):
    if source_id == 1:
        return u'web'
    return u'安卓'

def picture(pic_file):
    return current_app.config['STATIC_URL'] + pic_file


def activity_status(activity):
    if activity.is_closed:
        return u'活动被关闭'
    now = time.time()
    if now < activity.start_time:
        return ''
    if activity.start_time < now < activity.end_time:
        return u'正在进行中'
    return u'已经结束'


def get_type(type_id):
    return Type.query.get(type_id).type


def is_confirmed(confirmed):
    if confirmed:
        return u'审核通过'
    return u'未审核'
