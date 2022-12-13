from flask import Flask
from datetime import timedelta
from .configs import *
from my_news.utils.session import is_logged, is_its_account
from my_news.utils.files import posts_folder, users_folder
from my_news.utils.forms import service_fields


def create_app():
    app = Flask(__name__)
    app.permanent_session_lifetime = timedelta(days=15)
    app.config.from_mapping(**app_development)

    
    app.jinja_env.globals['service_fields'] = service_fields
    app.jinja_env.globals['isinstance'] = isinstance
    app.jinja_env.globals['is_logged'] = is_logged
    app.jinja_env.globals['is_its_account'] = is_its_account
    app.jinja_env.globals['posts_folder'] = posts_folder
    app.jinja_env.globals['users_folder'] = users_folder


    from .auth.route import auth
    from .posts.route import posts
    from .users.route import users
    from .about.route import about
    app.register_blueprint(auth)
    app.register_blueprint(posts)
    app.register_blueprint(users)
    app.register_blueprint(about)

    return app
