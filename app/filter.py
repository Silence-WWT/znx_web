# -*- coding: utf-8 -*-
import time


def stars(num):
    return '<i class="level_solid"></i>'*num + \
           '<i class="level_hollow"></i>'*(5-num)


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
