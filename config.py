# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # TODO: add a random string as the default SECRET_KEY.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'notification@znx.com'
    MAIL_PASSWORD = 'ntfc12345'
    ZNX_MAIL_SUBJECT_PREFIX = '[ZNX]'
    ZNX_MAIL_SENDER = 'Notification <Notification@znx.com>'
    PHOTO_DIR = '/web/static/'
    ORG_COMMENT_PER_PAGE = 10
    ADMIN_SESSIONS_PER_PAGE = 20
    ADMIN_REGISTER_PER_PAGE = 10
    ADMIN_ORG_PER_PAGE = 20
    STATIC_URL = 'http://static1.znx.com/'
    ADMIN_COMMENT_PER_PAGE = 20
    #CDN_DOMAIN = 'static1.znx.com'
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    CDN_DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://dev:devpassword@localhost/znx?charset=utf8'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://test:testpassword@localhost/znx_test?charset=utf8'


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql+pymysql://dbuser:usER_2014@node1.db/znx?charset=utf8'

# TODO: replace sqlite with mysql

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': ProductionConfig
}
