# -*- coding: utf-8 -*-
# TODO: mobile unicode 验证码 timefield: convert str time to epoch time.
import redis
import hashlib
from uuid import uuid4
from wtforms import Field
from wtforms.validators import ValidationError, Email


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


class EmptyEmail(Email):
    def __init__(self, message=None):
        super(EmptyEmail, self).__init__(message)

    def __call__(self, form, field):
        if field.data:
            super(EmptyEmail, self).__call__(form, field)

def generate_dir_path(org_id):
    return '%s/jigou_%s/' % (org_id%100, hashlib.sha1(str(org_id)).hexdigest())