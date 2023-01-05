from flask import Blueprint, render_template, request, jsonify
from .forms import *
import my_news.db.models as models
from my_news.utils.forms import set_values_to_form, get_values_from_form
from my_news.utils.session import logged_user
from my_news.utils.search import get_args


comments = Blueprint('comments', __name__)


@comments.route('/<int:news_id>', methods=['POST'])
def getall(news_id):
    fetched = models.comments.search(*get_args(request.form, 'body', 'posted_time'), news_id=news_id)
    if fetched:
        appended_comments = models.comments.appendone_getall(fetched, models.users, ['user_login', 'login'])
        return jsonify({'html': render_template('modules/comments.html', comments=appended_comments)})
    return jsonify({'html': render_template('modules/error.html', message='No comments yet')})


@comments.route('/add/<int:news_id>', methods=['POST'])
@logged_user.login_required
def add(news_id):
    form = CreateCommentForm()
    if request.form.get('first_load'):
        pass
    elif form.validate_on_submit():
        values = get_values_from_form(form)
        values['user_login'] = logged_user.info['login']
        values['news_id'] = news_id
        models.comments.add(**values)
        return jsonify({'status': True})
    return jsonify({'html': render_template('modules/form.html', form=form, object='comments_form')})


@comments.route('/edit/<int:id>', methods=['POST'])
@logged_user.login_required
def edit(id):
    form = CreateCommentForm()
    one_comment = models.comments.getone(id)
    if logged_user.is_its_account(one_comment['user_login']):
        if request.form.get('first_load'):
            pass
        elif form.validate_on_submit():
            values = get_values_from_form(form)
            models.comments.update(id, **values)
            return jsonify({'status': True})
        set_values_to_form(form, one_comment)
        return jsonify({'html': render_template('modules/modal_form.html', form=form)})
    return jsonify({'status': False})


@comments.route('/delete/<int:id>', methods=['POST'])
@logged_user.login_required
def delete(id):
    comment = models.comments.getone(id)
    if logged_user.is_its_account(comment['user_login']):
        models.comments.delete(id)
        return jsonify({'status': True})
    return jsonify({'status': False})