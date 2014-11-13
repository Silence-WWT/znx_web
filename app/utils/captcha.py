# -*- coding: utf-8 -*-
import redis
import requests
from random import seed, randint
from xml.dom import minidom


seed()


def send_captcha(user_or_org, mobile):
    local_redis = redis.StrictRedis(host='localhost', port=6379, db=0)
    rand = str(randint(100000, 999999))
    print 'generate round num:' + rand
    # r = send_sms(mobile, rand)
    # TODO: check return code by func send_sms.
    # print r.text
    status = send_sms(mobile, rand)
    if status:
        key = 'captcha:' + user_or_org + ':' + mobile
        local_redis.set(key, rand)
        local_redis.expire(key, 120)  # method set(key, rand, 120) may raise ResponseError on cloud server
        print 'get captcha:'
        print local_redis.get(key)
    return status


MESSAGE_API_CONTENT = u'尊敬的在哪学用户，您的验证码为%s，请您尽快完成操作，感谢您的使用！'
MESSAGE_API_CONTENT_TEST = u'您的验证码是：%s。请不要把验证码泄露给其他人。'
MESSAGE_API_SUCCESS = '2'


def send_sms(number, content):
    query = {'method': 'Submit',
             'account': 'cf_zainaxue',
             'password': 'zainaxue',
             'mobile': number,
             'content': MESSAGE_API_CONTENT % content}
    r = requests.get("http://106.ihuyi.cn/webservice/sms.php", params=query).text.encode('utf8')
    print r
    doc = minidom.parseString(r)
    status = doc.getElementsByTagName('code')[0].firstChild.nodeValue
    if status != MESSAGE_API_SUCCESS:
        return False
    else:
        return True

CONFIRM_MESSAGE = u'恭喜贵机构%s已通过在哪学网人工审核，登陆账号后可以正常添加课程和活动，更多问题请致电400-656-9191'


def send_confirm_sms(number, org_name):
    query = {'method': 'Submit',
             'account': 'cf_zainaxue',
             'password': 'zainaxue',
             'mobile': number,
             'content': CONFIRM_MESSAGE % org_name}
    r = requests.get("http://106.ihuyi.cn/webservice/sms.php", params=query).text.encode('utf8')
    print r
    doc = minidom.parseString(r)
    status = doc.getElementsByTagName('code')[0].firstChild.nodeValue
    if status != MESSAGE_API_SUCCESS:
        return False
    else:
        return True
