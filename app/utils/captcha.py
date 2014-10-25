# -*- coding: utf-8 -*-
import redis
import requests
from random import seed, randint


seed()


def send_captcha(user_or_org, mobile):
    local_redis = redis.StrictRedis(host='localhost', port=6379, db=0)
    rand = str(randint(100000, 999999))
    print 'generate round num:'+rand
    r = send_sms(mobile, rand)
    # TODO: check return code by func send_sms.
    print r.text
    key = 'captcha:'+user_or_org+':'+mobile
    local_redis.set(key, rand, 120)
    print 'get captcha:'
    print local_redis.get(key)


def send_sms(number, content):
    query = { 'method': 'Submit',
              'account': 'cf_znx',
              'password': 'znx123',
              'mobile': number,
              'content': u'您的验证码是：【%s】。请不要把验证码泄露给其他人。' % content}
    r = requests.get("http://106.ihuyi.cn/webservice/sms.php", params=query)
    return r
