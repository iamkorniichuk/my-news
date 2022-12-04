from flask import current_app, Blueprint, render_template, session, redirect, url_for
from my_news.forms import CreatePostForm
from my_news.models.posts import posts_model
from my_news.utils import login_required, save_file, POSTS_FOLDER, logged_user


posts = Blueprint('posts', __name__)


@posts.route('/')
@posts.route('/posts')
def all():
    allposts = posts_model.getallinorder({'key':'posted_time', 'reverse':False})
    return render_template('posts.html', title='News', posts=allposts)


@posts.route('/post/<id>')
def one(id):
    onepost = posts_model.getone(id)
    return render_template('post.html', title=onepost['title'], post=onepost)


@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    form = CreatePostForm()
    if form.validate_on_submit():
        # TODO: Check uniqueness
        posts_model.add(user_login=logged_user()['login'],
                        cover=save_file(form.cover.data, POSTS_FOLDER),
                        title=form.title.data,
                        body=form.body.data)
        return redirect(url_for('posts.all'))
    return render_template('create_post.html', title='Create', form=form)
