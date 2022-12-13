from flask import Blueprint, render_template, redirect, url_for, abort
from .forms import *
from my_news.models.posts import posts_model
from my_news.models.comments import comments_model
from my_news.utils.session import login_required, logged_user, is_its_account
from my_news.utils.files import save_file, posts_folder, delete_file, replace_file
from my_news.utils.forms import set_values_to_form, get_values_from_form


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
        return redirect(url_for('posts.one', id=id))
    return render_template('post.html', title=post['title'], post=post, form=form, comments=comments)


@posts.route('/post/create', methods=['POST', 'GET'])
@login_required
def create():
    form = CreatePostForm()
    if form.validate_on_submit():
        values = get_values_from_form(form)
        values['cover'] = save_file(values['cover'], posts_folder)
        posts_model.add(**values)
        return redirect(url_for('posts.all'))
    return render_template('create_post.html', title='Create', form=form)


@posts.route('/post/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit(id):
    # TODO: Dealt with edit/create form (create one or rename)
    form = CreatePostForm()
    post = posts_model.getone(id)
    if is_its_account(post['user_login']):
        if form.validate_on_submit():
            values = get_values_from_form(form)
            old_cover = post['cover']
            new_cover = values['cover']
            values['cover'] = replace_file(old_cover, new_cover, posts_folder())
            # TODO: Refresh info in session | Will it be better if use caching?
            posts_model.update(id, **values)
            return redirect(url_for('posts.one', id=id))
        set_values_to_form(form, post)
        return render_template('edit_post.html', title='Edit', form=form, id=id)
    abort(403)


@posts.route('/comment/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_comment(id):
    # TODO: Dealt with edit/create form (create one or rename)
    form = CreateCommentForm()
    comment = comments_model.getone(id)
    if is_its_account(comment['user_login']):
        if form.validate_on_submit():
            values = get_values_from_form(form)
            comments_model.update(id, **values)
            return redirect(url_for('posts.one', id=comment['post_id']))
        set_values_to_form(form, comment)
        return render_template('edit_comment.html', title='Edit', form=form, id=id)
    abort(403)


@posts.route('/comment/delete/<int:id>', methods=['POST'])
@login_required
def delete_comment(id):
    comment = comments_model.getone(id)
    if is_its_account(comment['user_login']):
        comments_model.delete(id)
        return redirect(url_for('posts.one', id=comment['post_id']))
    abort(403)


@posts.route('/post/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    post = posts_model.getone(id)
    if is_its_account(post['user_login']):
        delete_file(post['cover'], posts_folder())
        posts_model.delete(id)
        return redirect(url_for('posts.all'))
    abort(403)
