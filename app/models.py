# -*- coding: utf-8 -*-
from . import db, login_manager
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    # TODO: replace Boolean with BOOLEAN
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=True)
    email_confirmed = db.Column(db.Boolean, default=False)
    cellphone = db.Column(db.String(11), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    member_since = db.Column(db.TIMESTAMP)
    last_login = db.Column(db.TIMESTAMP)
    identity = db.Column(db.CHAR(44))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        from faker import Factory
        fake = Factory.create()
        zh = Factory.create('zh-CN')

        seed()
        for i in range(count):
            u = User(username=fake.user_name(),
                     email=fake.email(),
                     email_confirmed=True,
                     cellphone=zh.phone_number(),
                     password=fake.password(),
                     member_since=fake.date_time(),
                     last_login=fake.date_time(),
                     identity=fake.password(44)
                     )

            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Register(db.Model):
    __tablename__ = 'registers'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.Integer)
    cellphone = db.Column(db.CHAR(11))
    name = db.Column(db.Unicode(8))
    need = db.Column(db.Unicode(64))
    timestamp = db.Column(db.TIMESTAMP)


class SiteComment(db.Model):
    __tablename__ = 'site_comments'
    id = db.Column(db.Integer, primary_key=True)
    cellphone = db.Column(db.CHAR(11))
    body = db.Column(db.UnicodeText)
    timestamp = db.Column(db.TIMESTAMP)
    disabled = db.Column(db.Boolean)


class Organization(db.Model):
    __tablename__ = 'organizations'
    id = db.Column(db.Integer, primary_key=True)
    cellphone = db.Column(db.CHAR(11))
    password_hash = db.Column(db.String(128))
    member_since = db.Column(db.TIMESTAMP)
    type = db.Column(db.Integer)
    name = db.Column(db.Unicode(64))
    contact = db.Column(db.Unicode(16))
    address = db.Column(db.Unicode(256))
    authorization = db.Column(db.CHAR(32))
    photo = db.Column(db.CHAR(32))
    profession = db.Column(db.Integer)
    property = db.Column(db.Integer)
    size = db.Column(db.Integer)
    location = db.Column(db.Integer)
    confirmed = db.Column(db.Boolean)
    intro = db.Column(db.UnicodeText)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    page_view = db.Column(db.Integer)


class OrganizationComment(db.Model):
    __tablename__ = 'organization_comments'
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.Integer)
    user = db.Column(db.Integer)
    stars = db.Column(db.Integer)
    body = db.Column(db.UnicodeText)
    timestamp = db.Column(db.TIMESTAMP)
    disabled = db.Column(db.Boolean)


class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer)
    name = db.Column(db.Unicode(64))
    age_id = db.Column(db.Integer)
    price = db.Column(db.Integer)
    consult_time = db.Column(db.Unicode(64))
    start_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    try_ = db.Column(db.Boolean)
    timestamp = db.Column(db.TIMESTAMP)
    intro = db.Column(db.UnicodeText)
    closed = db.Column(db.Boolean)
    page_view = db.Column(db.Integer)


class ClassComment(db.Model):
    __tablename__ = 'classes_comments'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    stars = db.Column(db.Integer)
    body = db.Column(db.UnicodeText)
    timestamp = db.Column(db.TIMESTAMP)
    disabled = db.Column(db.Boolean)


class ClassTime(db.Model):
    __tablename__ = 'class_time'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer)
    time_id = db.Column(db.Integer)


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer)
    name = db.Column(db.Unicode(64))
    age_id = db.Column(db.Integer)
    price = db.Column(db.Integer)
    start_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    timestamp = db.Column(db.TIMESTAMP)
    intro = db.Column(db.UnicodeText)
    closed = db.Column(db.Boolean)
    page_view = db.Column(db.Integer)


class ActivityComment(db.Model):
    __tablename__ = 'activity_comments'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    stars = db.Column(db.Integer)
    body = db.Column(db.UnicodeText)
    timestamp = db.Column(db.TIMESTAMP)
    disabled = db.Column(db.Boolean)


# TODO: chart 等待魏鹏的方案


class ClassOrder(db.Model):
    __tablename__ = 'class_orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    class_id = db.Column(db.Integer)
    time = db.Column(db.Date)
    name = db.Column(db.Unicode(24))
    age = db.Column(db.Integer)
    sex = db.Column(db.Boolean)
    cellphone = db.Column(db.CHAR(11))
    address = db.Column(db.Unicode(128))
    timestamp = db.Column(db.TIMESTAMP)
    remark = db.Column(db.Unicode(100))
    canceled = db.Column(db.Boolean)


class ActivityOrder(db.Model):
    __tablename__ = 'activity_orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    activity_id = db.Column(db.Integer)
    time = db.Column(db.Date)
    name = db.Column(db.Unicode(24))
    age = db.Column(db.Integer)
    sex = db.Column(db.Boolean)
    cellphone = db.Column(db.CHAR(11))
    address = db.Column(db.Unicode(128))
    timestamp = db.Column(db.TIMESTAMP)
    remark = db.Column(db.Unicode(100))
    canceled = db.Column(db.Boolean)

class Time(db.Model):
    __tablename__ = 'times'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Unicode(16))

    @staticmethod
    def generate():
        db.session.add(Time(time=u'周一'))
        db.session.add(Time(time=u'周二'))
        db.session.add(Time(time=u'周三'))
        db.session.add(Time(time=u'周四'))
        db.session.add(Time(time=u'周五'))
        db.session.add(Time(time=u'周六'))
        db.session.add(Time(time=u'周日'))
        db.session.commit()

class Type(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Unicode(16))

    @staticmethod
    def generate():
        a = Type(type=u'学校')
        b = Type(type=u'机构')
        db.session.add(a)
        db.session.add(b)
        db.session.commit()




class Profession(db.Model):
    __tablename__ = 'professions'
    id = db.Column(db.Integer, primary_key=True)
    profession = db.Column(db.Unicode(16))

    @staticmethod
    def generate():
        db.session.add(Profession(profession=u'婴儿早教'))
        db.session.add(Profession(profession=u'幼儿培训'))
        db.session.add(Profession(profession=u'胎前课程'))
        db.session.commit()


class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    property = db.Column(db.Unicode(16))

    @staticmethod
    def generate():
        db.session.add(Property(property=u'国有'))
        db.session.add(Property(property=u'民营'))
        db.session.add(Property(property=u'外资'))
        db.session.add(Property(property=u'合资'))
        db.session.commit()


class Size(db.Model):
    __tablename__ = 'sizes'
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Unicode(16))

    @staticmethod
    def generate():
        db.session.add(Size(size=u'0-50'))
        db.session.add(Size(size=u'51-100'))
        db.session.add(Size(size=u'101-200'))
        db.session.add(Size(size=u'201-400'))
        db.session.add(Size(size=u'>400'))
        db.session.commit()


class Age(db.Model):
    __tablename__ = 'ages'
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Unicode(64))

    @staticmethod
    def generate():
        db.session.add(Age(age=u'0-6个月'))
        db.session.add(Age(age=u'6-12个月'))
        db.session.add(Age(age=u'1-2岁'))
        db.session.add(Age(age=u'2-4岁'))
        db.session.add(Age(age=u'学龄前'))
        db.session.commit()


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.Unicode(6))
    district = db.Column(db.Unicode(9))

    @staticmethod
    def generate():
        db.session.add(Location(city=u'西安', district=u'雁塔区'))
        db.session.add(Location(city=u'西安', district=u'长安区'))
        db.session.add(Location(city=u'北京', district=u'海淀区'))
        db.session.commit()
