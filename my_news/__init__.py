from flask import Flask
from datetime import timedelta
from my_news.utils import is_logged


def create_app():
    app = Flask(__name__)
    app.permanent_session_lifetime = timedelta(days=15)
    app.config.update(
        TESTING=True,
        SECRET_KEY='password'
    )
    app.jinja_env.globals['is_logged'] = is_logged


    from .routes.auth import auth
    from .routes.posts import posts
    from .routes.users import users
    from .routes.about import about
    app.register_blueprint(auth)
    app.register_blueprint(posts)
    app.register_blueprint(users)
    app.register_blueprint(about)

    return app
