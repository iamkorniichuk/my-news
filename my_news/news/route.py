from flask import Blueprint, render_template, redirect, request, url_for, abort, jsonify, json
from .forms import *
from my_news.models.news import news_model
from my_news.models.comments import comments_model
from my_news.utils.session import login_required, logged_user, is_its_account, admin_required
from my_news.utils.files import save_file, news_folder, delete_file, replace_file
from my_news.utils.forms import set_values_to_form, get_values_from_form


news = Blueprint('news', __name__)


@news.route('/', methods=['POST', 'GET'])
@news.route('/news', methods=['POST', 'GET'])
def all():
    # TODO: To end creating
    form = CreateNewsForm()
    if form.validate_on_submit():
        create_news(form)
        return redirect(url_for('news.all'))
    # TODO: To end search
    if request.args:
        order = None
        key = request.form.get('key')
        reverse = request.form.get('reverse')
        if key or reverse:
            order = {}
            order['key'] = key
            order['reverse'] = reverse
        news = news_model.getall()
        return jsonify({'htmlresponse': render_template('news_cover.html', news=news)})
    news = news_model.getall({'key':'posted_time', 'reverse':False})
    return render_template('news.html', title='News', news=news, form=form)


def create_news(form):
    # TODO: To end creating
    values = get_values_from_form(form)
    values['user_login'] = logged_user()['login']
    values['cover'] = save_file(values['cover'], news_folder())
    news_model.add(**values)


@news.route('/history', methods=['POST', 'GET'])
def history():
    if request.method == 'POST':
        ids = request.form['history']
        if ids:
            history = []
            for id in json.loads(ids):
                news = news_model.getone(id)
                if news:
                    history.append(news)
            history.reverse()
            return jsonify({'htmlresponse': render_template('news_covers.html', news=history)})
        else:
            return jsonify({'htmlresponse': render_template('error.html', message='No news in history yet')})
    return render_template('history.html', title='History')


@news.route('/news/<int:id>')
def one(id):
    form = CreateCommentForm()
    news = news_model.getone(id)
    comments = comments_model.getall({'key':'posted_time', 'reverse':False}, news_id=id)
    if form.validate_on_submit():
        comments_model.add(user_login=logged_user()['login'],
                            news_id=id,
                            body=form.body.data)
        return redirect(url_for('news.one', id=id))
    return render_template('one_news.html', title=news['title'], news=news, form=form, comments=comments)


@news.route('/news/edit/<int:id>', methods=['POST'])
@admin_required
def edit(id):
    form = CreateNewsForm()
    news = news_model.getone(id)
    # TODO: Show error only if form doesn't validate
    if is_its_account(news['user_login']):
        if request.form.get('show'):
            pass
        elif form.validate_on_submit():
            values = get_values_from_form(form)
            old_cover = news['cover']
            new_cover = values['cover']
            values['cover'] = replace_file(old_cover, new_cover, news_folder())
            news_model.update(id, **values)
            return jsonify({'urlresponse': url_for('news.all')})
        set_values_to_form(form, news)
        return jsonify({'htmlresponse': render_template('modal_form.html', form=form, action=url_for('news.edit', id=id))})
    abort(403)


@news.route('/news/delete/<int:id>', methods=['POST'])
@admin_required
def delete(id):
    post = news_model.getone(id)
    if is_its_account(post['user_login']):
        delete_file(post['cover'], news_folder())
        news_model.delete(id)
        return redirect(url_for('news.all'))
    abort(403)


@news.route('/comment/edit/<int:id>', methods=['POST'])
@login_required
def edit_comment(id):
    # TODO: Dealt with edit/create form (create one or rename)
    form = CreateCommentForm()
    comment = comments_model.getone(id)
    if is_its_account(comment['user_login']):
        if form.validate_on_submit():
            values = get_values_from_form(form)
            comments_model.update(id, **values)
            return redirect(url_for('news.one', id=comment['post_id']))
        set_values_to_form(form, comment)
        return render_template('edit_comment.html', title='Edit', form=form, id=id)
    abort(403)


@news.route('/comment/delete/<int:id>', methods=['POST'])
@login_required
def delete_comment(id):
    comment = comments_model.getone(id)
    if is_its_account(comment['user_login']):
        comments_model.delete(id)
        return redirect(url_for('news.one', id=comment['post_id']))
    abort(403)


