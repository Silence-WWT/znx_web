# -*- coding: utf-8 -*-
# TODO: mobile unicode 验证码 timefield: convert str time to epoch time.
import redis
from wtforms import Field
from wtforms.validators import ValidationError


class Captcha(object):
    def __init__(self, user_or_org, mobile_field, message=None):
        self.user_or_org = user_or_org
        self.mobile_field = mobile_field
        if not message:
            message = u'验证码错误'
        self.message = message

    def __call__(self, form, field):
        local_redis = redis.StrictRedis(host='localhost', port=6379, db=0)
        key = 'captcha:'+self.user_or_org+':'+form[self.mobile_field].data
        redis_value = local_redis.get(key)
        if redis_value != field.data:
            raise ValidationError(self.message)