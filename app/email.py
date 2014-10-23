# -*- coding: utf-8 -*-
import requests
from flask.ext.mail import Message
from flask import current_app, render_template
from . import mail


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['ZNX_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['ZNX_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
# TODO: add redis-queue.


def send_sms(number, content):
    query = { 'method': 'Submit',
              'account': 'cf_znx',
              'password': 'znx123',
              'mobile': number,
              'content': u'您的验证码是：【%s】。请不要把验证码泄露给别人' % content}
    r = requests.get("http://106.ihuyi.cn/webservice/sms.php", params=query)
    return r

