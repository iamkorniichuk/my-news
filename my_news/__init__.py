from flask import Flask
from datetime import timedelta
from .configs import *
from my_news.utils import is_logged, is_logged_user, posts_file, users_file


def create_app():
    app = Flask(__name__)
    app.permanent_session_lifetime = timedelta(days=15)
    app.config.from_mapping(**App().development)
    app.jinja_env.globals['is_logged'] = is_logged
    app.jinja_env.globals['is_logged_user'] = is_logged_user
    app.jinja_env.globals['posts_file'] = posts_file
    app.jinja_env.globals['users_file'] = users_file


    from .routes.auth import auth
    from .routes.posts import posts
    from .routes.users import users
    from .routes.about import about
    app.register_blueprint(auth)
    app.register_blueprint(posts)
    app.register_blueprint(users)
    app.register_blueprint(about)

    return app
