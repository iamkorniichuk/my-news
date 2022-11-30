from flask import Blueprint, render_template, session, redirect, url_for
# from my_news.forms.posts import EditForm, CreateForm
from my_news.models.posts import posts_model
from my_news.utils import login_required


posts = Blueprint('posts', __name__)


@posts.route('/')
@posts.route('/posts')
@login_required
def all():
    return render_template('posts.html', title='News', posts=posts_model.getall())
