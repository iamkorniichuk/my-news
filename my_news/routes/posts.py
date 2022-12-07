from flask import Blueprint, render_template, redirect, url_for
from my_news.forms import CreatePostForm, CreateCommentForm
from my_news.models.posts import posts_model
from my_news.models.comments import comments_model
from my_news.utils.session import login_required, logged_user
from my_news.utils.files import save_file, posts_folder, delete_file


posts = Blueprint('posts', __name__)


@posts.route('/')
@posts.route('/posts')
def all():
    allposts = posts_model.getallinorder({'key':'posted_time', 'reverse':False})
    return render_template('posts.html', title='News', posts=allposts)


@posts.route('/post/<int:id>', methods=['POST', 'GET'])
def one(id):
    form = CreateCommentForm()
    post = posts_model.getone(id)
    comments = comments_model.getallinorder({'key':'posted_time', 'reverse':False}, post_id=id)
    if form.validate_on_submit():
        comments_model.add(user_login=logged_user()['login'],
                            post_id=id,
                            body=form.body.data)
        return redirect(url_for('posts.one', id=id), code=302)
    return render_template('post.html', title=post['title'], post=post, form=form, comments=comments)


@posts.route('/post/create', methods=['POST', 'GET'])
@login_required
def create():
    form = CreatePostForm()
    if form.validate_on_submit():
        posts_model.add(user_login=logged_user()['login'],
                        cover=save_file(form.cover.data, posts_folder()),
                        title=form.title.data,
                        body=form.body.data)
        return redirect(url_for('posts.all'))
    return render_template('create_post.html', title='Create', form=form)


@login_required
@posts.route('/post/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    form = CreatePostForm()
    post = posts_model.getone(id)
    if form.validate_on_submit():
        delete_file(post['cover'], posts_folder())
        posts_model.update(id, user_login=logged_user()['login'],
                        cover=save_file(form.cover.data, posts_folder()),
                        title=form.title.data,
                        body=form.body.data)
        return redirect(url_for('posts.one', id=id))
    form.cover.data = post['cover']
    form.title.data = post['title']
    form.body.data = post['body']
    return render_template('edit_post.html', title='Edit', form=form, id=id)


@login_required
@posts.route('/post/delete/<int:id>', methods=['POST'])
def delete(id):
    post = posts_model.getone(id)
    delete_file(post['cover'], posts_folder())
    posts_model.delete(id)
    return redirect(url_for('posts.all'), code=302)
