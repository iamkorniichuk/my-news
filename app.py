from flask import Flask, request, render_template
from wtforms import SubmitField, MultipleFileField, RadioField
from flask_wtf.file import FileField
from wtforms.csrf.core import CSRFTokenField
from my_news.configs import *
from my_news.utils.session import logged_user



app = Flask(__name__)
app.template_folder = 'my_news/templates'
app.static_folder = 'my_news/static'
app.config.from_mapping(**app_development)


@app.errorhandler(Exception)
def error(error):
    if request.method == 'GET':
        return render_template('pages/error.html', title='Error', header='Something went wrong!', message=error.description)
    return render_template('modules/error.html', message=error.description)

    
app.jinja_env.globals['SubmitField'] = SubmitField
app.jinja_env.globals['CSRFTokenField'] = CSRFTokenField
app.jinja_env.globals['MultipleFileField'] = MultipleFileField
app.jinja_env.globals['FileField'] = FileField
app.jinja_env.globals['RadioField'] = RadioField
app.jinja_env.globals['isinstance'] = isinstance
app.jinja_env.globals['logged_user'] = logged_user
app.jinja_env.globals['request'] = request


from my_news.blueprints.auth.route import auth
from my_news.blueprints.news.route import news
from my_news.blueprints.users.route import users
from my_news.blueprints.comments.route import comments
from my_news.blueprints.reviews.route import reviews
from my_news.blueprints.history.route import history
from my_news.blueprints.pages.route import pages
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(news, url_prefix='/news')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(comments, url_prefix='/comments')
app.register_blueprint(reviews, url_prefix='/reviews')
app.register_blueprint(history, url_prefix='/history')
app.register_blueprint(pages)

