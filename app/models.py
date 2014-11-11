# -*- coding: utf-8 -*-
import time
from uuid import uuid4
from . import db, login_manager
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session


class AnonymousUser(AnonymousUserMixin):
    def get_unified_id(self):
        if 'uuid' in session:
            uuid = session['uuid']
            unified_id = UnifiedId.query.filter_by(web_key=uuid).first()
            if unified_id:
                return unified_id.id
        uuid = uuid4().hex
        unified_id = UnifiedId(user_id=0,
                               web_key=uuid,
                               mobile_key='',
                               created=time.time())
        db.session.add(unified_id)
        db.session.commit()
        session['uuid'] = uuid
        return unified_id.id

    def reg_unified_id(self):
        if 'uuid' in session:
            uuid = session['uuid']
            unified_id = UnifiedId.query.filter_by(web_key=uuid).first()
            if unified_id and (unified_id.user_id == 0):
                return unified_id.id
        uuid = uuid4().hex
        unified_id = UnifiedId(user_id=0,
                               web_key=uuid,
                               mobile_key='',
                               created=time.time())
        db.session.add(unified_id)
        db.session.commit()
        session['uuid'] = uuid
        return unified_id.id

login_manager.anonymous_user = AnonymousUser

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    # id
    id = db.Column(db.Integer, primary_key=True)
    # 用户名 4-16 Unicode
    username = db.Column(db.Unicode(16), nullable=False)
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

    def get_unified_id(self):
        unified_id = UnifiedId.query.filter_by(user_id=self.id).first_or_404()
        return unified_id.id

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
            u = User(username=zh.name(),
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
    name = db.Column(db.Unicode(16), nullable=False)
    # 需求 <=16 Unicode
    need = db.Column(db.Unicode(16), nullable=False)
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
    # 手机号 qq号 邮箱
    contact = db.Column(db.String(32), nullable=False)
    # 留言信息 140 Unicode
    body = db.Column(db.Unicode(140), nullable=False)
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
            u = SiteComment(contact=zh.phone_number(),
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
    name = db.Column(db.Unicode(255), default=u'', nullable=False)
    # 广告 30 Unicode
    slogan = db.Column(db.Unicode(30), default=u'', nullable=False)
    # 联系人 6 Unicode
    contact = db.Column(db.Unicode(6), default=u'', nullable=False)
    # 联系电话 35 Unicode
    contract_phone = db.Column(db.Unicode(255), default=u'', nullable=False)
    # 地址 100 Unicode
    address = db.Column(db.Unicode(100), default=u'', nullable=False)
    # 执照照片
    authorization = db.Column(db.String(255), default='', nullable=False)
    # 门店照片
    photo = db.Column(db.String(255), default='', nullable=False)
    # LOGO照片
    logo = db.Column(db.String(255), default='', nullable=False)
    # 区域
    location_id = db.Column(db.Integer, default=0, nullable=False)
    # 是否被认证
    is_confirmed = db.Column(db.BOOLEAN, default=False, nullable=False)
    # 附近交通 200 Unicode
    traffic = db.Column(db.Unicode(200), default=u'', nullable=False)
    # 移动端 经纬度
    longitude = db.Column(db.Float, default=0.0, nullable=False)
    latitude = db.Column(db.Float, default=0.0, nullable=False)
    # 页面浏览量
    page_view = db.Column(db.Integer, default=0, nullable=False)
    # 官方网站
    site = db.Column(db.CHAR(255), nullable=False)
    # 详情 UnicodeText
    detail = db.Column(db.UnicodeText, default=u'', nullable=False)
    # 评论数量
    comment_count = db.Column(db.Integer, default=0, nullable=False)
    # 评价
    star = db.Column(db.Float, default=0.0, nullable=False)
    # 报名数
    orders = db.Column(db.Integer, default=0, nullable=False)

    def set_star(self, star):
        stars = self.star * self.comment_count
        self.comment_count += 1
        self.star = (stars + star) / self.comment_count

    def add_orders(self):
        self.orders += 1

    def page_view_inc(self):
        self.page_view += 1

    @property
    def location(self):
        location = Location.query.get(self.location_id)
        return location.get_location()

    def get_comment_count(self):
        return OrganizationComment.query.\
            filter_by(organization_id=self.id).count()

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

    def get_sign_up_num(self):
        class_order_num = ClassOrder.query.filter(ClassOrder.class_id.in_(
            db.session.query(Class.id).filter(Class.organization_id==self.id)
        )).count()

        activity_order_num = ActivityOrder.query.filter(ActivityOrder.activity_id.in_(
        db.session.query(Activity.id).filter(Activity.organization_id==self.id)
        )).count()
        return class_order_num+activity_order_num

    def get_name(self):
        return self.name or self.mobile

    def get_ages(self):
        age_ids = OrganizationAge.query.filter_by(organization_id=self.id).all()
        ages = list()
        for age_id in age_ids:
            ages.append(Age.query.get(age_id.age_id))
        return ages

    def get_professions(self):
        profession_ids = OrganizationProfession.query.\
            filter_by(organization_id=self.id).all()
        professions = list()
        for profession_id in profession_ids:
            professions.append(Profession.query.get(profession_id.profession_id))
        return professions


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

        seed()
        for i in range(count):
            u = Organization(mobile=zh.phone_number(),
                             password=fake.password(),
                             created=time.mktime(fake.date_time().timetuple()),
                             type_id=randint(1, type_count),
                             name=zh.company(),
                             slogan=u'学技术到蓝翔',
                             contact=zh.name(),
                             contract_phone=zh.phone_number(),
                             address=zh.address(),
                             authorization='',
                             photo='',
                             logo='',
                             location_id=randint(1, location_count),
                             is_confirmed=True,
                             detail=zh.text(),
                             traffic=u'太白南路',
                             longitude=zh.longitude(),
                             latitude=zh.latitude(),
                             site='www.baidu.com',
                             page_view=randint(0, 10000))
            db.session.add(u)
            db.session.commit()


class OrganizationAge(db.Model):
    __tablename__ = 'organization_ages'
    __table_args__ = (
        db.UniqueConstraint(
            'organization_id', 'age_id', name='unq_org_age'
        ),
    )
    id = db.Column(db.Integer, primary_key=True)
    # 机构 id
    organization_id = db.Column(db.Integer, nullable=False)
    # 年龄 id
    age_id = db.Column(db.Integer, nullable=False)

    @staticmethod
    def generate_fake():
        from random import seed, sample
        org_count = Organization.query.count()
        age_count = Age.query.count()
        age_range = range(1, age_count+1)

        seed()
        for org_id in range(1, org_count+1):
            for age_id in sample(age_range, 3):
                u = OrganizationAge(organization_id=org_id, age_id=age_id)
                db.session.add(u)
            db.session.commit()


class OrganizationProfession(db.Model):
    __tablename__ = 'organization_professions'
    __table_args__ = (
        db.UniqueConstraint(
            'organization_id', 'profession_id', name='unq_org_profession'
        ),
    )
    id = db.Column(db.Integer, primary_key=True)
    # 机构 id
    organization_id = db.Column(db.Integer, nullable=False)
    # 行业  id
    profession_id = db.Column(db.Integer, nullable=False)

    @staticmethod
    def generate_fake():
        from random import seed, sample
        org_count = Organization.query.count()
        profession_count = Profession.query.count()
        profession_range = range(1, profession_count+1)

        seed()
        for org_id in range(1, org_count+1):
            for profession_id in sample(profession_range, 3):
                u = OrganizationProfession(organization_id=org_id, profession_id=profession_id)
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
    body = db.Column(db.Unicode(140), nullable=False)
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
                    body=zh.sentence(),
                    created=time.mktime(fake.date_time().timetuple()))
                db.session.add(u)
            db.session.commit()


class UnifiedId(db.Model):
    __tablename__ = 'unified_id'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    mobile_key = db.Column(db.CHAR(64), nullable=False)
    web_key = db.Column(db.CHAR(32), nullable=False)
    created = db.Column(db.Integer, nullable=False)

    def get_mobile(self):
        return User.query.get(self.user_id).mobile


class ChatLine(db.Model):
    __tablename__ = 'chat_lines'
    id = db.Column(db.Integer, primary_key=True)
    unified_id = db.Column(db.Integer, nullable=False)
    is_user = db.Column(db.BOOLEAN, nullable=False)
    content = db.Column(db.Unicode(100), nullable=False)
    # web 1 android 2
    source = db.Column(db.Integer, nullable=False)
    organization_id = db.Column(db.Integer, nullable=False)
    created = db.Column(db.Integer, nullable=False)

    def get_user(self):
        user_id = UnifiedId.query.get(self.unified_id).user_id
        return User.query.get(user_id)

    def get_org(self):
        return db.session.query(Organization.name).\
            filter(Organization.id==self.organization_id)


class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    # 机构id
    organization_id = db.Column(db.Integer, nullable=False)
    # 课程名字 30 Unicode
    name = db.Column(db.Unicode(255), nullable=False)
    # 价格
    price = db.Column(db.Unicode(30), default=u'', nullable=False)
    # 咨询时间 20 Unicode
    consult_time = db.Column(db.Unicode(20), nullable=False)
    # 是否可以免费试听
    is_tastable = db.Column(db.BOOLEAN, nullable=False)
    # 创建时间
    created = db.Column(db.Integer, nullable=False)
    # 滚动开班
    is_round = db.Column(db.BOOLEAN, nullable=False)
    # 天数
    days = db.Column(db.Integer, nullable=False)
    # 关闭
    is_closed = db.Column(db.BOOLEAN, default=False, nullable=False)
    # 浏览量
    page_view = db.Column(db.Integer, default=0, nullable=False)
    # 详情
    detail = db.Column(db.UnicodeText, nullable=False)
    # 图片
    photo = db.Column(db.String(255), nullable=False)

    def get_org(self):
        return Organization.query.get(self.organization_id)

    def get_comment_count(self):
        return ClassComment.query.filter_by(class_id=self.id).count()

    def get_comments(self):
        return ClassComment.query.filter_by(class_id=self.id).all()

    def get_ages(self):
        age_ids = ClassAge.query.filter_by(class_id=self.id).all()
        ages = list()
        for age_id in age_ids:
            ages.append(Age.query.get(age_id.age_id))
        return ages

    def get_time(self):
        classtimes = ClassTime.query.filter_by(class_id=self.id).all()
        class_time = unicode()
        for classtime in classtimes:
            class_time += Time.query.get(classtime.time_id).time
        return class_time

    @property
    def stars(self):
        stars = db.session.query(ClassComment.stars). \
            filter(ClassComment.class_id==self.id).all()
        if stars:
            sumary = 0
            for star in stars:
                sumary += star.stars
            return sumary/len(stars)
        else:
            return 0

    @staticmethod
    def generate_fake(count=20):
        from faker import Factory
        from random import seed, randint
        fake = Factory.create()
        zh = Factory.create('zh-CN')
        organization_count = Organization.query.count()

        seed()
        for organization_id in range(1, organization_count+1):
            for i in range(count):
                u = Class(organization_id=organization_id,
                          name=u'课程名字',
                          price=unicode(randint(0, 100000)),
                          consult_time=unicode(zh.word()),
                          is_tastable=True,
                          is_round=True,
                          days=randint(10,20),
                          created=time.mktime(fake.date_time().timetuple()),
                          detail=zh.text(),
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
    body = db.Column(db.Unicode(140), nullable=False)
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
                    body=zh.sentence(),
                    created=fake.unix_time())
                db.session.add(u)
            db.session.commit()


class ClassTime(db.Model):
    __tablename__ = 'class_time'
    __table_args__ = (
        db.UniqueConstraint(
            'class_id', 'time_id', name='unq_class_time'
        ),
    )
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


class ClassAge(db.Model):
    __tablename__ = 'class_age'
    __table_args__ = (
        db.UniqueConstraint(
            'class_id', 'age_id', name='unq_class_age'
        ),
    )
    id = db.Column(db.Integer, primary_key=True)
    # 课程
    class_id = db.Column(db.Integer, nullable=False)
    # 年龄
    age_id = db.Column(db.Integer, nullable=False)

    @staticmethod
    def generate_fake():
        from random import seed, sample
        class_count = Class.query.count()
        age_count = Age.query.count()
        age_range = range(1, age_count+1)

        seed()
        for class_id in range(1, class_count+1):
            for age_id in sample(age_range, 3):
                u = ClassAge(class_id=class_id, age_id=age_id)
                db.session.add(u)
            db.session.commit()


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    # 机构
    organization_id = db.Column(db.Integer, nullable=False)
    # 活动名字 255 Unicode
    name = db.Column(db.Unicode(255), nullable=False)
    # 价格
    price = db.Column(db.Unicode(30), default=u'', nullable=False)
    # 创建时间
    created = db.Column(db.Integer, nullable=False)
    # 起始时间
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)
    # 图片
    photo = db.Column(db.CHAR(255), default='', nullable=False)
    # 关闭
    is_closed = db.Column(db.BOOLEAN, default=False, nullable=False)
    # 浏览量
    page_view = db.Column(db.Integer, default=0, nullable=False)
    # 活动类型
    category_id = db.Column(db.Integer, nullable=False)
    # 区县
    location_id = db.Column(db.Integer, default=0, nullable=False)
    # 地址 40 Unicode
    address = db.Column(db.Unicode(40), default=u'', nullable=False)
    # 地标 40 Unicode
    landmark = db.Column(db.Unicode(40), default=u'', nullable=False)
    # 附近交通 200
    traffic = db.Column(db.Unicode(200), default=u'', nullable=False)
    # 联系方式 255 Unicode
    contract_phone = db.Column(db.Unicode(255), default=u'', nullable=False)
    # 详情
    detail = db.Column(db.UnicodeText, default=u'', nullable=False)

    def get_comment_count(self):
        return ActivityComment.query.filter_by(activity_id=self.id).count()

    def get_ages(self):
        age_ids = ActivityAge.query.filter_by(activity_id=self.id).all()
        ages = list()
        for age_id in age_ids:
            ages.append(Age.query.get(age_id.age_id))
        return ages

    def get_comments(self):
        return ActivityComment.query.filter_by(activity_id=self.id).all()

    def get_org(self):
        return Organization.query.get(self.organization_id)

    def get_time(self):
        return time.ctime(self.start_time)+'~'+time.ctime(self.end_time)

    @property
    def location(self):
        location = Location.query.get(self.location_id)
        return location.get_location()

    @property
    def stars(self):
        stars = db.session.query(ActivityComment.stars). \
            filter(ActivityComment.activity_id==self.id).all()
        if stars:
            sumary = 0
            for star in stars:
                sumary += star.stars
            return sumary/len(stars)
        else:
            return 0

    @staticmethod
    def generate_fake(count=20):
        from faker import Factory
        from random import seed, randint
        fake = Factory.create()
        zh = Factory.create('zh-CN')
        organization_count = Organization.query.count()
        category_count = Category.query.count()

        seed()
        for organization_id in range(1, organization_count+1):
            for i in range(count):
                u = Activity(organization_id=organization_id,
                             name=zh.word(),
                             price=unicode(randint(0, 100000)),
                             start_time=fake.unix_time(),
                             end_time=fake.unix_time(),
                             created=fake.unix_time(),
                             detail=zh.text(),
                             contract_phone=zh.phone_number(),
                             address=zh.address(),
                             landmark=zh.word(),
                             traffic=zh.sentence(),
                             is_closed=False,
                             category_id=randint(1, category_count),
                             page_view=randint(1, 10000))
                db.session.add(u)
                db.session.commit()


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    # 活动类型 10 Unicode
    category = db.Column(db.Unicode(10), nullable=False)

    @staticmethod
    def generate():
        db.session.add(Category(category=u'室内活动'))
        db.session.add(Category(category=u'户外活动'))
        db.session.add(Category(category=u'儿童剧'))
        db.session.add(Category(category=u'展览'))
        db.session.add(Category(category=u'音乐会/演出'))
        db.session.add(Category(category=u'爱心公益'))
        db.session.add(Category(category=u'比赛讲座'))
        db.session.commit()


class ActivityAge(db.Model):
    __tablename__ = 'activity_age'
    __table_args__ = (
        db.UniqueConstraint(
            'activity_id', 'age_id', name='unq_activity_age'
        ),
    )
    id = db.Column(db.Integer, primary_key=True)
    # 活动
    activity_id = db.Column(db.Integer, nullable=False)
    # 年龄
    age_id = db.Column(db.Integer, nullable=False)

    @staticmethod
    def generate_fake():
        from random import seed, sample
        activity_count = Activity.query.count()
        age_count = Age.query.count()
        age_range = range(1, age_count+1)

        seed()
        for activity_id in range(1, activity_count+1):
            for age_id in sample(age_range, 3):
                u = ActivityAge(activity_id=activity_id, age_id=age_id)
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
    body = db.Column(db.Unicode(140), nullable=False)
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
                    body=unicode((zh.sentence())),
                    created=fake.unix_time())
                db.session.add(u)
            db.session.commit()


class ClassOrder(db.Model):
    __tablename__ = 'class_orders'
    id = db.Column(db.Integer, primary_key=True)
    # 用户
    unified_id = db.Column(db.Integer, nullable=False)
    # 课程
    class_id = db.Column(db.Integer, nullable=False)
    # 创建时间
    created = db.Column(db.Integer, nullable=False)
    # 试听时间
    time = db.Column(db.Integer, nullable=False)
    # 听课人 6 Unicode
    name = db.Column(db.Unicode(6), nullable=False)
    # 年龄 10 Unicode
    age = db.Column(db.Unicode(10), nullable=False)
    # 性别
    sex = db.Column(db.BOOLEAN, nullable=False)
    # 手机号
    mobile = db.Column(db.CHAR(11), nullable=False)
    # email
    email = db.Column(db.String(64), nullable=False)
    # 地址 40 Unicode
    address = db.Column(db.Unicode(40), nullable=False)
    # 备注 100 Unicode
    remark = db.Column(db.Unicode(100), nullable=False)
    # 取消
    is_canceled = db.Column(db.BOOLEAN, default=False, nullable=False)
    # 提交订单
    is_submitted = db.Column(db.BOOLEAN, default=False, nullable=False)

    def get_class(self):
        return Class.query.get(self.class_id)

    def get_time(self):
        return time.strftime('%Y/%m/%d %H:%M', time.localtime(self.time))

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
                    unified_id=randint(1, user_count),
                    created=fake.unix_time(),
                    name=zh.name(),
                    age=unicode(randint(1, 10)),
                    sex=True,
                    mobile=zh.phone_number(),
                    email=zh.email(),
                    address=zh.address(),
                    remark=u'备注',
                    time=fake.unix_time())
                db.session.add(u)
            db.session.commit()


class ActivityOrder(db.Model):
    __tablename__ = 'activity_orders'
    id = db.Column(db.Integer, primary_key=True)
    # 用户
    unified_id = db.Column(db.Integer, nullable=False)
    # 活动
    activity_id = db.Column(db.Integer, nullable=False)
    # 创建时间
    created = db.Column(db.Integer, nullable=False)
    # 姓名 6 Unicode
    name = db.Column(db.Unicode(6), nullable=False)
    # 年龄 10 Unicode
    age = db.Column(db.Unicode(10), nullable=False)
    # 性别
    sex = db.Column(db.BOOLEAN, nullable=False)
    # 手机号
    mobile = db.Column(db.CHAR(11), nullable=False)
    # email
    email = db.Column(db.String(64), nullable=False)
    # 地址
    address = db.Column(db.Unicode(40), nullable=False)
    # 备注
    remark = db.Column(db.Unicode(100), nullable=False)
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
                    unified_id=randint(1, user_count),
                    created=fake.unix_time(),
                    email=fake.email(),
                    name=zh.name(),
                    age=unicode(randint(1, 10)),
                    sex=True,
                    mobile=zh.phone_number(),
                    address=zh.address(),
                    remark=zh.sentence())
                db.session.add(u)
            db.session.commit()


class Time(db.Model):
    __tablename__ = 'times'
    id = db.Column(db.Integer, primary_key=True)
    # 上课时间 6 Unicode
    time = db.Column(db.Unicode(6), nullable=False)

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
    type = db.Column(db.Unicode(6), nullable=False)

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
    profession = db.Column(db.Unicode(8), nullable=False, unique=True)

    @staticmethod
    def generate():
        db.session.add(Profession(profession=u'语言类'))
        db.session.add(Profession(profession=u'启蒙类'))
        db.session.add(Profession(profession=u'才艺类'))
        db.session.commit()


class Age(db.Model):
    __tablename__ = 'ages'
    id = db.Column(db.Integer, primary_key=True)
    # 适应年龄 10 Unicode
    age = db.Column(db.Unicode(10), nullable=False, unique=True)

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
    __table_args__ = (
        db.UniqueConstraint(
            'city_id', 'district', name='unq_city_district'
        ),
    )
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, nullable=False)
    # 区县 6
    district = db.Column(db.Unicode(6), nullable=False)

    def get_location(self):
        city = City.query.get(self.city_id)
        return city.city + u' - '+ self.district

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
    city = db.Column(db.Unicode(5), nullable=False, unique=True)


def generate_helper_data():
    Location.generate()
    Age.generate()
    Profession.generate()
    Type.generate()
    Time.generate()
    Category.generate()


def generate_fake_data(org_num=50, org_comment=30,
                       class_num=10, class_order=10, class_com=10,
                       act_num=10, act_order=10, act_com=10):
    Register.generate_fake()
    SiteComment.generate_fake()
    User.generate_fake()
    Organization.generate_fake(org_num)
    OrganizationAge.generate_fake()
    OrganizationProfession.generate_fake()
    OrganizationComment.generate_fake(org_comment)
    Class.generate_fake(class_num)
    ClassComment.generate_fake(class_com)
    ClassOrder.generate_fake(class_order)
    ClassAge.generate_fake()

    ClassTime.generate_fake()

    Activity.generate_fake(act_num)
    ActivityAge.generate_fake()
    ActivityComment.generate_fake(act_com)
    ActivityOrder.generate_fake(act_order)
