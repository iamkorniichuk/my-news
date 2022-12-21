from flask import Flask
from wtforms import SubmitField
from wtforms.csrf.core import CSRFTokenField
from datetime import timedelta
from .configs import *
from my_news.utils.session import is_logged, is_its_account, is_admin, logged_user
from my_news.utils.files import news_folder, users_folder


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(**app_development)

    
    app.jinja_env.globals['SubmitField'] = SubmitField
    app.jinja_env.globals['CSRFTokenField'] = CSRFTokenField
    app.jinja_env.globals['isinstance'] = isinstance
    app.jinja_env.globals['is_logged'] = is_logged
    app.jinja_env.globals['logged_user'] = logged_user
    app.jinja_env.globals['is_admin'] = is_admin
    app.jinja_env.globals['is_its_account'] = is_its_account
    app.jinja_env.globals['news_folder'] = news_folder
    app.jinja_env.globals['users_folder'] = users_folder


    from .auth.route import auth
    from .news.route import news
    from .users.route import users
    from .about.route import about
    app.register_blueprint(auth)
    app.register_blueprint(news)
    app.register_blueprint(users)
    app.register_blueprint(about)

    return app
