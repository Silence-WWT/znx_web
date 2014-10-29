# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.rq import RQ
from flask.ext.principal import Principal
from flask_debugtoolbar import DebugToolbarExtension
from config import config
from .filter import stars, sex, get_date_time
from .permission import config_identity

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
rq = RQ()
principal = Principal()
login_manager = LoginManager()
debug_tool_bar = DebugToolbarExtension()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    rq.init_app(app)
    login_manager.init_app(app)
    debug_tool_bar.init_app(app)
    principal.init_app(app)

    config_identity(app)

    app.jinja_env.filters['stars'] = stars
    app.jinja_env.filters['sex'] = sex
    app.jinja_env.filters['get_date_time'] = get_date_time

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    from .org import org as org_blueprint
    app.register_blueprint(org_blueprint, url_prefix='/org')

    from .course import course as course_blueprint
    app.register_blueprint(course_blueprint, url_prefix='/course')

    from .activity import activity as activity_blueprint
    app.register_blueprint(activity_blueprint, url_prefix='/activity')

    from .test import test as test_blueprint
    app.register_blueprint(test_blueprint, url_prefix='/test')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
