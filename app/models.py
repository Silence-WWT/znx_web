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
    # TODO: last_login redis
    # last_login = db.Column(db.TIMESTAMP)
    identity = db.Column(db.CHAR(44))

    def get_id(self):
        return u'u'+unicode(self.id)

    def get_name(self):
        return self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_fake(count=1000):
        from sqlalchemy.exc import IntegrityError
        from faker import Factory
        fake = Factory.create()
        zh = Factory.create('zh-CN')

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
    if user_id[0] == u'o':
        return Organization.query.get(int(user_id[1:]))
    return User.query.get(int(user_id[1:]))


class Register(db.Model):
    __tablename__ = 'registers'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.Integer)
    cellphone = db.Column(db.CHAR(11))
    name = db.Column(db.Unicode(8))
    need = db.Column(db.Unicode(64))
    timestamp = db.Column(db.TIMESTAMP)

    @staticmethod
    def generate_fake(count=1000):
        from faker import Factory
        from random import seed, randint
        fake = Factory.create()
        zh = Factory.create('zh-CN')
        location_count = Location.query.count()

        seed()
        for i in range(count):
            u = Register(location=randint(1, location_count),
                         cellphone=zh.phone_number(),
                         name=unicode(zh.name()),
                         need=unicode(zh.job()),
                         timestamp=fake.date_time())

            db.session.add(u)
            db.session.commit()


class SiteComment(db.Model):
    __tablename__ = 'site_comments'
    id = db.Column(db.Integer, primary_key=True)
    cellphone = db.Column(db.CHAR(11))
    body = db.Column(db.UnicodeText)
    timestamp = db.Column(db.TIMESTAMP)
    disabled = db.Column(db.Boolean, default=False)

    @staticmethod
    def generate_fake(count=1000):
        from faker import Factory
        from random import seed
        fake = Factory.create()
        zh = Factory.create('zh-CN')

        seed()
        for i in range(count):
            u = SiteComment(cellphone=zh.phone_number(),
                            body=zh.text(),
                            timestamp=fake.date_time())

            db.session.add(u)
            db.session.commit()


class Organization(UserMixin, db.Model):
    __tablename__ = 'organizations'
    id = db.Column(db.Integer, primary_key=True)
    cellphone = db.Column(db.CHAR(11))
    password_hash = db.Column(db.String(128))
    member_since = db.Column(db.TIMESTAMP)
    type = db.Column(db.Integer)
    name = db.Column(db.Unicode(256))
    contact = db.Column(db.Unicode(16))
    address = db.Column(db.Unicode(512))
    authorization = db.Column(db.CHAR(32))
    photo = db.Column(db.CHAR(32))
    profession = db.Column(db.Integer)
    property_ = db.Column(db.Integer)
    size = db.Column(db.Integer)
    location = db.Column(db.Integer)
    confirmed = db.Column(db.Boolean)
    intro = db.Column(db.UnicodeText)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    page_view = db.Column(db.Integer)

    def get_id(self):
        return 'o'+unicode(self.id)

    def get_name(self):
        return self.name or self.cellphone

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_fake(count=50):
        from faker import Factory
        from random import seed, randint
        fake = Factory.create()
        zh = Factory.create('zh-CN')
        location_count = Location.query.count()
        type_count = Type.query.count()
        profession_count = Profession.query.count()
        property_count = Property.query.count()
        size_count = Size.query.count()

        seed()
        for i in range(count):
            u = Organization(cellphone=zh.phone_number(),
                             password=fake.password(),
                             member_since=fake.date_time(),
                             type=randint(1, type_count),
                             name=zh.company(),
                             contact=zh.name(),
                             address=zh.address(),
                             authorization='1'*32,
                             photo='1'*32,
                             profession=randint(1, profession_count),
                             property_=randint(1, property_count),
                             size=randint(1, size_count),
                             location=randint(1, location_count),
                             confirmed=True,
                             intro=zh.text(),
                             longitude=zh.longitude(),
                             latitude=zh.latitude(),
                             page_view=randint(0, 10000))
            db.session.add(u)
            db.session.commit()


class OrganizationComment(db.Model):
    __tablename__ = 'organization_comments'
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    stars = db.Column(db.Integer)
    body = db.Column(db.UnicodeText)
    timestamp = db.Column(db.TIMESTAMP)
    disabled = db.Column(db.Boolean, default=False)

    @staticmethod
    def generate_fake(count=50):
        from faker import Factory
        from random import seed, randint
        fake = Factory.create()
        zh = Factory.create('zh-CN')
        organization_count = Organization.query.count()
        user_count = User.query.count()

        seed()
        for organization_id in range(1, organization_count+1):
            for i in range(count):
                u = OrganizationComment(
                    organization_id=organization_id,
                    user_id=randint(1, user_count),
                    stars=randint(1, 5),
                    body=zh.text(),
                    timestamp=fake.date_time())
                db.session.add(u)
                db.session.commit()


class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer)
    name = db.Column(db.Unicode(256))
    age_id = db.Column(db.Integer)
    price = db.Column(db.Integer)
    consult_time = db.Column(db.Unicode(128))
    start_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    try_ = db.Column(db.Boolean)
    timestamp = db.Column(db.TIMESTAMP)
    intro = db.Column(db.UnicodeText)
    closed = db.Column(db.Boolean, default=False)
    page_view = db.Column(db.Integer)

    @staticmethod
    def generate_fake(count=20):
        from faker import Factory
        from random import seed, randint
        fake = Factory.create()
        zh = Factory.create('zh-CN')
        organization_count = Organization.query.count()
        age_count = Age.query.count()

        seed()
        for organization_id in range(1, organization_count+1):
            for i in range(count):
                u = Class(organization_id=organization_id,
                          name=zh.text(),
                          age_id=randint(1, age_count),
                          price=randint(0, 100000),
                          consult_time=zh.sentence(),
                          start_time=fake.date_time(),
                          end_time=fake.date_time(),
                          try_=True,
                          timestamp=fake.date_time(),
                          intro=zh.text(),
                          closed=False,
                          page_view=randint(1, 10000))
                db.session.add(u)
                db.session.commit()


class ClassComment(db.Model):
    # TODO：confirm joined.
    __tablename__ = 'classes_comments'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    stars = db.Column(db.Integer)
    body = db.Column(db.UnicodeText)
    timestamp = db.Column(db.TIMESTAMP)
    disabled = db.Column(db.Boolean, default=False)

    @staticmethod
    def generate_fake(count=20):
        from faker import Factory
        from random import seed, randint
        fake = Factory.create()
        zh = Factory.create('zh-CN')
        class_count = Class.query.count()
        user_count = User.query.count()

        seed()
        for class_id in range(1, class_count+1):
            for i in range(count):
                u = ClassComment(
                    class_id=class_id,
                    user_id=randint(1, user_count),
                    stars=randint(1, 5),
                    body=zh.text(),
                    timestamp=fake.date_time())
                db.session.add(u)
            db.session.commit()


class ClassTime(db.Model):
    __tablename__ = 'class_time'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer)
    time_id = db.Column(db.Integer)

    @staticmethod
    def generate_fake():
        from random import seed, sample
        class_count = Class.query.count()
        time_count = Time.query.count()
        time_range = range(1, time_count+1)

        seed()
        for class_id in range(1, class_count+1):
            for time_id in sample(time_range, 3):
                u = ClassTime(class_id=class_id, time_id=time_id)
                db.session.add(u)
            db.session.commit()


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer)
    name = db.Column(db.Unicode(256))
    age_id = db.Column(db.Integer)
    price = db.Column(db.Integer)
    start_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    timestamp = db.Column(db.TIMESTAMP)
    intro = db.Column(db.UnicodeText)
    closed = db.Column(db.Boolean, default=False)
    page_view = db.Column(db.Integer)

    @staticmethod
    def generate_fake(count=20):
        from faker import Factory
        from random import seed, randint
        fake = Factory.create()
        zh = Factory.create('zh-CN')
        organization_count = Organization.query.count()
        age_count = Age.query.count()

        seed()
        for organization_id in range(1, organization_count+1):
            for i in range(count):
                u = Activity(organization_id=organization_id,
                             name=zh.text(),
                             age_id=randint(1, age_count),
                             price=randint(0, 100000),
                             start_time=fake.date_time(),
                             end_time=fake.date_time(),
                             timestamp=fake.date_time(),
                             intro=zh.text(),
                             closed=False,
                             page_view=randint(1, 10000))
                db.session.add(u)
                db.session.commit()


class ActivityComment(db.Model):
    __tablename__ = 'activity_comments'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    stars = db.Column(db.Integer)
    body = db.Column(db.UnicodeText)
    timestamp = db.Column(db.TIMESTAMP)
    disabled = db.Column(db.Boolean, default=False)

    @staticmethod
    def generate_fake(count=20):
        from faker import Factory
        from random import seed, randint
        fake = Factory.create()
        zh = Factory.create('zh-CN')
        activity_count = Activity.query.count()
        user_count = User.query.count()

        seed()
        for activity_id in range(1, activity_count+1):
            for i in range(count):
                u = ActivityComment(
                    activity_id=activity_id,
                    user_id=randint(1, user_count),
                    stars=randint(1, 5),
                    body=zh.text(),
                    timestamp=fake.date_time())
                db.session.add(u)
            db.session.commit()


# TODO: chart 等待魏鹏的方案


class ClassOrder(db.Model):
    __tablename__ = 'class_orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    class_id = db.Column(db.Integer)
    time = db.Column(db.TIMESTAMP)
    name = db.Column(db.Unicode(24))
    age = db.Column(db.Integer)
    sex = db.Column(db.Boolean)
    cellphone = db.Column(db.CHAR(11))
    address = db.Column(db.Unicode(128))
    timestamp = db.Column(db.TIMESTAMP)
    remark = db.Column(db.Unicode(300))
    canceled = db.Column(db.Boolean, default=False)

    @staticmethod
    def generate_fake(count=100):
        from faker import Factory
        from random import seed, randint
        fake = Factory.create()
        zh = Factory.create('zh-CN')
        class_count = Class.query.count()
        user_count = User.query.count()

        seed()
        for class_id in range(1, class_count+1):
            for i in range(count):
                u = ClassOrder(
                    class_id=class_id,
                    user_id=randint(1, user_count),
                    time=fake.date_time(),
                    name=zh.name(),
                    age=randint(1, 10),
                    sex=True,
                    cellphone=zh.phone_number(),
                    address=zh.address(),
                    timestamp=fake.date_time(),
                    remark=zh.text())
                db.session.add(u)
            db.session.commit()


class ActivityOrder(db.Model):
    __tablename__ = 'activity_orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    activity_id = db.Column(db.Integer)
    time = db.Column(db.TIMESTAMP)
    name = db.Column(db.Unicode(24))
    age = db.Column(db.Integer)
    sex = db.Column(db.Boolean)
    cellphone = db.Column(db.CHAR(11))
    address = db.Column(db.Unicode(128))
    timestamp = db.Column(db.TIMESTAMP)
    remark = db.Column(db.Unicode(300))
    canceled = db.Column(db.Boolean)

    @staticmethod
    def generate_fake(count=100):
        from faker import Factory
        from random import seed, randint
        fake = Factory.create()
        zh = Factory.create('zh-CN')
        activity_count = Activity.query.count()
        user_count = User.query.count()

        seed()
        for activity_id in range(1, activity_count+1):
            for i in range(count):
                u = ActivityOrder(
                    activity_id=activity_id,
                    user_id=randint(1, user_count),
                    time=fake.date_time(),
                    name=zh.name(),
                    age=randint(1, 10),
                    sex=True,
                    cellphone=zh.phone_number(),
                    address=zh.address(),
                    timestamp=fake.date_time(),
                    remark=zh.text())
                db.session.add(u)
            db.session.commit()


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


def generate_helper_data():
    Location.generate()
    Age.generate()
    Size.generate()
    Property.generate()
    Profession.generate()
    Type.generate()
    Time.generate()


def generate_fake_data():
    Register.generate_fake()
    SiteComment.generate_fake()
    User.generate_fake()
    Organization.generate_fake()
    OrganizationComment.generate_fake()
    Class.generate_fake()
    ClassComment.generate_fake()
    ClassOrder.generate_fake()

    ClassTime.generate_fake()

    Activity.generate_fake()
    ActivityComment.generate_fake()
    ActivityOrder.generate_fake()
