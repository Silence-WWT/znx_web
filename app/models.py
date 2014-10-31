# -*- coding: utf-8 -*-
import time
from . import db, login_manager
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    # id
    id = db.Column(db.Integer, primary_key=True)
    # 用户名 4-16 Unicode
    username = db.Column(db.Unicode(48), nullable=False)
    # 邮箱
    email = db.Column(db.String(64), nullable=False)
    # 邮箱确认
    is_email_confirmed = db.Column(db.BOOLEAN, default=False, nullable=False)
    # 手机号
    mobile = db.Column(db.CHAR(11), nullable=False)
    # 哈希后的密码
    password_hash = db.Column('password', db.String(128), nullable=False)
    # 注册时间
    created = db.Column(db.Integer, nullable=False)
    # 移动端标识
    identity = db.Column(db.String(64), nullable=False)

    def get_id(self):
        return u'u'+unicode(self.id)

    def get_name(self):
        return self.username

    def is_org(self):
        return False

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
                     is_email_confirmed=True,
                     mobile=zh.phone_number(),
                     password=fake.password(),
                     created=time.mktime(fake.date_time().timetuple()),
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
    # id
    id = db.Column(db.Integer, primary_key=True)
    # 求学地址
    city_id = db.Column(db.Integer, nullable=False)
    # 手机号
    mobile = db.Column(db.CHAR(11), nullable=False)
    # 名字 4-16 Unicode
    name = db.Column(db.Unicode(48), nullable=False)
    # 需求 <=6 Unicode
    need = db.Column(db.Unicode(18), nullable=False)
    # 创建时间
    created = db.Column(db.Integer, nullable=False)

    def get_date(self):
        return time.strftime('[%Y-%m-%d]', time.localtime(self.created))


    @staticmethod
    def generate_fake(count=1000):
        from faker import Factory
        from random import seed, randint
        fake = Factory.create()
        zh = Factory.create('zh-CN')
        city_count = City.query.count()

        seed()
        for i in range(count):
            u = Register(city_id=randint(1, city_count),
                         mobile=zh.phone_number(),
                         name=unicode(zh.name()),
                         need=unicode(zh.name()),
                         created=time.mktime(fake.date_time().timetuple()))

            db.session.add(u)
            db.session.commit()


class SiteComment(db.Model):
    __tablename__ = 'site_comments'
    id = db.Column(db.Integer, primary_key=True)
    # 手机号码
    # TODO: 变更为手机号 qq号  邮箱 增加长度。
    mobile = db.Column(db.String(11), nullable=False)
    # 留言信息 140 Unicode
    body = db.Column(db.Unicode(420), nullable=False)
    # 创建时间
    created = db.Column(db.Integer, nullable=False)
    # 被关闭
    is_disabled = db.Column(db.BOOLEAN, default=False, nullable=False)

    @staticmethod
    def generate_fake(count=1000):
        from faker import Factory
        from random import seed
        fake = Factory.create()
        zh = Factory.create('zh-CN')

        seed()
        for i in range(count):
            u = SiteComment(mobile=zh.phone_number(),
                            body=u'很好',
                            created=time.mktime(fake.date_time().timetuple()))

            db.session.add(u)
            db.session.commit()


class Organization(UserMixin, db.Model):
    __tablename__ = 'organizations'
    id = db.Column(db.Integer, primary_key=True)
    # 手机号
    mobile = db.Column(db.CHAR(11), nullable=False)
    # 哈希后的密码
    password_hash = db.Column('password', db.String(128), nullable=False)
    # 注册时间
    created = db.Column(db.Integer, nullable=False)
    # 类型
    type_id = db.Column(db.Integer, default=0, nullable=False)
    # 机构名 30Unicode
    name = db.Column(db.Unicode(90), default=u'', nullable=False)
    # 广告 30 Unicode
    slogan = db.Column(db.Unicode(90), default=u'', nullable=False)
    # 联系人 6 Unicode
    contact = db.Column(db.Unicode(18), default=u'', nullable=False)
    # 地址 40 Unicode
    address = db.Column(db.Unicode(120), default=u'', nullable=False)
    # 执照照片
    authorization = db.Column(db.CHAR(36), default='', nullable=False)
    # 门店照片
    photo = db.Column(db.CHAR(36), default='', nullable=False)
    # LOGO照片
    logo = db.Column(db.CHAR(36), default='', nullable=False)
    # 行业
    profession_id = db.Column(db.Integer, default=0, nullable=False)
    # 类别
    property_id = db.Column(db.Integer, default=0, nullable=False)
    # 规模
    size_id = db.Column(db.Integer, default=0, nullable=False)
    # 区域
    location_id = db.Column(db.Integer, default=0, nullable=False)
    # 是否被认证
    is_confirmed = db.Column(db.BOOLEAN, default=False, nullable=False)
    # 介绍 140 Unicode
    intro = db.Column(db.Unicode(420), default=u'', nullable=False)
    # 附近交通 30 Unicode
    traffic = db.Column(db.Unicode(90), default=u'', nullable=False)
    # 移动端 经纬度
    longitude = db.Column(db.Float, default=0.0, nullable=False)
    latitude = db.Column(db.Float, default=0.0, nullable=False)
    # 页面浏览量
    page_view = db.Column(db.Integer, default=0, nullable=False)

    def get_comments(self):
        return OrganizationComment.query.\
            filter_by(organization_id=self.id).all()

    def get_classes(self):
        return Class.query.\
            filter_by(organization_id=self.id).all()

    def get_activities(self):
        return Activity.query.\
            filter_by(organization_id=self.id).all()

    def get_id(self):
        return u'o'+unicode(self.id)

    def is_org(self):
        return True

    def get_name(self):
        return self.name or self.mobile

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
            u = Organization(mobile=zh.phone_number(),
                             password=fake.password(),
                             created=time.mktime(fake.date_time().timetuple()),
                             type_id=randint(1, type_count),
                             name=zh.company(),
                             slogan=u'学技术到蓝翔',
                             contact=zh.name(),
                             address=zh.address(),
                             authorization='1'*36,
                             photo='1'*36,
                             logo='1'*36,
                             profession_id=randint(1, profession_count),
                             property_id=randint(1, property_count),
                             size_id=randint(1, size_count),
                             location_id=randint(1, location_count),
                             is_confirmed=True,
                             intro=zh.text(),
                             traffic=u'太白南路',
                             longitude=zh.longitude(),
                             latitude=zh.latitude(),
                             page_view=randint(0, 10000))
            db.session.add(u)
            db.session.commit()


class OrganizationComment(db.Model):
    __tablename__ = 'organization_comments'
    id = db.Column(db.Integer, primary_key=True)
    # 机构id
    organization_id = db.Column(db.Integer, nullable=False)
    # 用户id
    user_id = db.Column(db.Integer, nullable=False)
    # 评价
    stars = db.Column(db.SMALLINT, nullable=False)
    # 评价内容 140 Unicode
    body = db.Column(db.Unicode(420), nullable=False)
    # 创建时间
    created = db.Column(db.Integer, nullable=False)
    # 被关闭
    is_disabled = db.Column(db.BOOLEAN, default=False, nullable=False)

    def get_user(self):
        return User.query.get(self.user_id)

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
                    created=time.mktime(fake.date_time().timetuple()))
                db.session.add(u)
            db.session.commit()


class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    # 机构id
    organization_id = db.Column(db.Integer, nullable=False)
    # 课程名字 30 Unicode
    name = db.Column(db.Unicode(90), nullable=False)
    # 年龄
    age_id = db.Column(db.Integer, nullable=False)
    # 价格
    price = db.Column(db.Integer, nullable=False)
    # 咨询时间 20 Unicode
    consult_time = db.Column(db.Unicode(60), nullable=False)
    # 是否可以免费试听
    is_tastable = db.Column(db.BOOLEAN, nullable=False)
    # 创建时间
    created = db.Column(db.Integer, nullable=False)
    # 滚动开班
    is_round = db.Column(db.BOOLEAN, nullable=False)
    # 天数
    days = db.Column(db.Integer, nullable=False)
    # 课程简介 140 Unicode
    intro = db.Column(db.Unicode(420), nullable=False)
    # 关闭
    is_closed = db.Column(db.BOOLEAN, default=False, nullable=False)
    # 浏览量
    page_view = db.Column(db.Integer, default=0, nullable=False)

    def get_org(self):
        return Organization.query.get(self.organization_id)

    def get_comment_count(self):
        return ClassComment.query.filter_by(class_id=self.id).count()

    def get_comments(self):
        return ClassComment.query.filter_by(class_id=self.id).all()

    def get_age(self):
        return Age.query.get(self.age_id).age

    def get_time(self):
        classtimes = ClassTime.query.filter_by(class_id=self.id).all()
        class_time = unicode()
        for classtime in classtimes:
            class_time += Time.query.get(classtime.time_id).time
        return class_time


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
                          name=u'课程名字',
                          age_id=randint(1, age_count),
                          price=randint(0, 100000),
                          consult_time=unicode(zh.words()),
                          is_tastable=True,
                          is_round=True,
                          days=randint(10,20),
                          created=time.mktime(fake.date_time().timetuple()),
                          intro=zh.text(),
                          is_closed=False,
                          page_view=randint(1, 10000))
                db.session.add(u)
                db.session.commit()


class ClassComment(db.Model):
    # TODO：confirm joined.
    __tablename__ = 'classes_comments'
    id = db.Column(db.Integer, primary_key=True)
    # 课程
    class_id = db.Column(db.Integer, nullable=False)
    # 用户
    user_id = db.Column(db.Integer, nullable=False)
    # 评价
    stars = db.Column(db.SMALLINT, nullable=False)
    # 评价内容 140 Unicode
    body = db.Column(db.Unicode(420), nullable=False)
    # 评价时间
    created = db.Column(db.Integer, nullable=False)
    # 被关闭
    is_disabled = db.Column(db.BOOLEAN, default=False, nullable=False)

    def get_user(self):
        return User.query.get(self.user_id)

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
                    body=unicode((zh.text())),
                    created=fake.unix_time())
                db.session.add(u)
            db.session.commit()


class ClassTime(db.Model):
    __tablename__ = 'class_time'
    id = db.Column(db.Integer, primary_key=True)
    # 课程
    class_id = db.Column(db.Integer, nullable=False)
    # 时间
    time_id = db.Column(db.Integer, nullable=False)

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
    # 机构
    organization_id = db.Column(db.Integer, nullable=False)
    # 活动名字 30 Unicode
    name = db.Column(db.Unicode(90), nullable=False)
    # 年龄
    age_id = db.Column(db.Integer, nullable=False)
    # 价格
    price = db.Column(db.Integer, nullable=False)
    # 创建时间
    created = db.Column(db.Integer, nullable=False)
    # 起始时间
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)
    # 活动简介 140 Unicode
    intro = db.Column(db.Unicode(420), nullable=False)
    # 图片
    photo = db.Column(db.CHAR(36), default='', nullable=False)
    # 关闭
    is_closed = db.Column(db.BOOLEAN, default=False, nullable=False)
    # 浏览量
    page_view = db.Column(db.Integer, default=0, nullable=False)

    def get_comment_count(self):
        return ActivityComment.query.filter_by(activity_id=self.id).count()

    def get_age(self):
        return Age.query.get(self.age_id).age

    def get_comments(self):
        return ActivityComment.query.filter_by(activity_id=self.id).all()

    def get_org(self):
        return Organization.query.get(self.organization_id)

    def get_time(self):
        return time.ctime(self.start_time)+'~'+time.ctime(self.end_time)

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
                             name=zh.word(),
                             age_id=randint(1, age_count),
                             price=randint(0, 100000),
                             start_time=fake.unix_time(),
                             end_time=fake.unix_time(),
                             created=fake.unix_time(),
                             intro=zh.text(),
                             is_closed=False,
                             page_view=randint(1, 10000))
                db.session.add(u)
                db.session.commit()


class ActivityComment(db.Model):
    __tablename__ = 'activity_comments'
    id = db.Column(db.Integer, primary_key=True)
    # 活动
    activity_id = db.Column(db.Integer, nullable=False)
    # 用户
    user_id = db.Column(db.Integer, nullable=False)
    # 评价
    stars = db.Column(db.SMALLINT, nullable=False)
    # 评价内容 140 Unicode
    body = db.Column(db.Unicode(420), nullable=False)
    # 创建时间
    created = db.Column(db.Integer, nullable=False)
    # 关闭
    is_disabled = db.Column(db.BOOLEAN, default=False, nullable=False)

    def get_user(self):
        return User.query.get(self.user_id)

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
                    body=unicode((zh.text())),
                    created=fake.unix_time())
                db.session.add(u)
            db.session.commit()


# TODO: chart 等待魏鹏的方案


class ClassOrder(db.Model):
    __tablename__ = 'class_orders'
    id = db.Column(db.Integer, primary_key=True)
    # 用户
    user_id = db.Column(db.Integer, nullable=False)
    # 课程
    class_id = db.Column(db.Integer, nullable=False)
    # 创建时间
    created = db.Column(db.Integer, nullable=False)
    # 试听时间
    time = db.Column(db.Integer, nullable=False)
    # 听课人 6 Unicode
    name = db.Column(db.Unicode(18), nullable=False)
    # 年龄 10 Unicode
    age = db.Column(db.Unicode(30), nullable=False)
    # 性别
    sex = db.Column(db.BOOLEAN, nullable=False)
    # 手机号
    mobile = db.Column(db.CHAR(11), nullable=False)
    # email
    email = db.Column(db.String(64), nullable=False)
    # 地址 40 Unicode
    address = db.Column(db.Unicode(120), nullable=False)
    # 校区 20 Unicode
    campus = db.Column(db.Unicode(60), nullable=False)
    # 备注 100 Unicode
    remark = db.Column(db.Unicode(300), nullable=False)
    # 取消
    is_canceled = db.Column(db.BOOLEAN, default=False, nullable=False)
    # 提交订单
    is_submitted = db.Column(db.BOOLEAN, default=False, nullable=False)

    def get_class(self):
        return Class.query.get(self.class_id)

    def get_time(self):
        return time.ctime(self.time)

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
                    created=fake.unix_time(),
                    name=zh.name(),
                    age=unicode(randint(1, 10)),
                    sex=True,
                    mobile=zh.phone_number(),
                    email=zh.email(),
                    address=zh.address(),
                    campus=u'通天苑校区',
                    remark=u'备注',
                    time=fake.unix_time())
                db.session.add(u)
            db.session.commit()


class ActivityOrder(db.Model):
    __tablename__ = 'activity_orders'
    id = db.Column(db.Integer, primary_key=True)
    # 用户
    user_id = db.Column(db.Integer, nullable=False)
    # 活动
    activity_id = db.Column(db.Integer, nullable=False)
    # 创建时间
    created = db.Column(db.Integer, nullable=False)
    # 姓名 6 Unicode
    name = db.Column(db.Unicode(18), nullable=False)
    # 年龄 10 Unicode
    age = db.Column(db.Unicode(30), nullable=False)
    # 性别
    sex = db.Column(db.BOOLEAN, nullable=False)
    # 手机号
    mobile = db.Column(db.CHAR(11), nullable=False)
    # email
    email = db.Column(db.String(64), nullable=False)
    # 地址
    address = db.Column(db.Unicode(120), nullable=False)
    # 备注
    remark = db.Column(db.Unicode(300), nullable=False)
    # 取消
    is_canceled = db.Column(db.BOOLEAN, default=False, nullable=False)
    # 提交订单
    is_submitted = db.Column(db.BOOLEAN, default=False, nullable=False)

    def get_activity(self):
        return Activity.query.get(self.activity_id)

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
                    created=fake.unix_time(),
                    email=fake.email(),
                    name=zh.name(),
                    age=unicode(randint(1, 10)),
                    sex=True,
                    mobile=zh.phone_number(),
                    address=zh.address(),
                    remark=zh.text())
                db.session.add(u)
            db.session.commit()


class Time(db.Model):
    __tablename__ = 'times'
    id = db.Column(db.Integer, primary_key=True)
    # 上课时间 6 Unicode
    time = db.Column(db.Unicode(18), nullable=False)

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
    # 类型 6 Unicode
    type = db.Column(db.Unicode(18), nullable=False)

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
    # 行业 8 Unicode
    profession = db.Column(db.Unicode(24), nullable=False)

    @staticmethod
    def generate():
        db.session.add(Profession(profession=u'婴儿早教'))
        db.session.add(Profession(profession=u'幼儿培训'))
        db.session.add(Profession(profession=u'胎前课程'))
        db.session.commit()


class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    # 类别 6 Unicode
    property = db.Column(db.Unicode(18), nullable=False)

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
    # 规模 6 Unicode
    size = db.Column(db.Unicode(18), nullable=False)

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
    # 适应年龄 10 Unicode
    age = db.Column(db.Unicode(30), nullable=False)

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
    city_id = db.Column(db.Integer, nullable=False)
    # 区县 4
    district = db.Column(db.Unicode(12), nullable=False)

    @staticmethod
    def generate():
        beijing =City(city=u'北京')
        xian =City(city=u'西安')
        db.session.add(beijing)
        db.session.add(xian)
        db.session.commit()

        db.session.add(Location(city_id=xian.id, district=u'雁塔区'))
        db.session.add(Location(city_id=xian.id, district=u'长安区'))
        db.session.add(Location(city_id=beijing.id, district=u'海淀区'))
        db.session.commit()

class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    # 城市 5 Unicode
    city = db.Column(db.Unicode(15), nullable=False)

def generate_helper_data():
    Location.generate()
    Age.generate()
    Size.generate()
    Property.generate()
    Profession.generate()
    Type.generate()
    Time.generate()


def generate_fake_data(org_num=50, org_comment=30,
                       class_num=10, class_order=10, class_com=10,
                       act_num=10, act_order=10, act_com=10):
    Register.generate_fake()
    SiteComment.generate_fake()
    User.generate_fake()
    Organization.generate_fake(org_num)
    OrganizationComment.generate_fake(org_comment)
    Class.generate_fake(class_num)
    ClassComment.generate_fake(class_com)
    ClassOrder.generate_fake(class_order)

    ClassTime.generate_fake()

    Activity.generate_fake(act_num)
    ActivityComment.generate_fake(act_com)
    ActivityOrder.generate_fake(act_order)
