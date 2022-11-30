from flask import Flask
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    app.permanent_session_lifetime = timedelta(days=15)
    app.config.update(
        TESTING=True,
        SECRET_KEY='password'
    )

    from .routes.auth import auth
    from .routes.posts import posts
    app.register_blueprint(auth)
    app.register_blueprint(posts)

    return app
