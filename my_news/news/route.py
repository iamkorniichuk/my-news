from flask import Blueprint, render_template, redirect, request, url_for, abort, jsonify, json
from .forms import *
from my_news.models.users import users_model
from my_news.models.news import news_model
from my_news.models.comments import comments_model
from my_news.utils.session import login_required, logged_user, is_its_account, admin_required, is_admin
from my_news.utils.files import save_file, save_files, news_folder, delete_file, delete_files, replace_files, replace_file
from my_news.utils.forms import set_values_to_form, get_values_from_form


news = Blueprint('news', __name__)


@news.route('/', methods=['POST', 'GET'])
@news.route('/news', methods=['POST', 'GET'])
def all():
    form = CreateNewsForm()
    if form.validate_on_submit():
        values = get_values_from_form(form)
        values['user_login'] = logged_user()['login']
        values['cover'] = save_file(values['cover'], news_folder())
        values['images'] = save_files(values['images'], news_folder())
        news_model.add(**values)
        return redirect(url_for('news.all'))
    # TODO: To end search
    fetched = news_model.search('title', request.args.get('search'), {'key':'posted_time', 'reverse':False})
    news = news_model.appendone_getall(fetched, users_model, ['user_login', 'login'])
    if is_admin():
        info = {}
        info['users'] = users_model.count()
        info['news'] = news_model.count()
        info['comments'] = comments_model.count()
        return render_template('news.html', title='News', news=news, form=form, info=info)
    return render_template('news.html', title='News', news=news, form=form)



@news.route('/history', methods=['POST', 'GET'])
def history():
    if request.method == 'POST':
        ids = request.form['history']
        if ids:
            history = []
            for id in json.loads(ids):
                news = news_model.appendone_getone(news_model.getone(id), users_model, ['user_login', 'login'])
                if news:
                    history.append(news)
            history.reverse()
            return jsonify({'htmlresponse': render_template('news_covers.html', news=history)})
        else:
            return jsonify({'htmlresponse': render_template('error.html', message='No news in history yet')})
    return render_template('history.html', title='History')


@news.route('/news/<int:id>', methods=['POST', 'GET'])
def one(id):
    form = CreateCommentForm()
    news = news_model.appendone_getone(news_model.getone(id), users_model, ['user_login', 'login'])
    if news['images']:
        news['images'].insert(0, news['cover'])
    else:
        news['images'] = None
    if form.validate_on_submit():
        values = get_values_from_form(form)
        values['user_login'] = logged_user()['login']
        values['news_id'] = id
        comments_model.add(**values)
        return redirect(url_for('news.one', id=id))
    return render_template('one_news.html', title=news['title'], news=news, form=form)


@news.route('/news/edit/<int:id>', methods=['POST'])
@admin_required
def edit(id):
    form = CreateNewsForm()
    news = news_model.getone(id)
    if is_its_account(news['user_login']):
        if request.form.get('show'):
            pass
        elif form.validate_on_submit():
            values = get_values_from_form(form)
            old_cover = news['cover']
            new_cover = values['cover']
            old_images = news['images']
            new_images = values['images']
            values['cover'] = replace_file(old_cover,  new_cover, news_folder())
            if old_images and new_images:
                values['images'] = replace_files(old_images,  new_images, news_folder())
            elif old_images:
                delete_files(old_images, news_folder())
            elif new_images:
                values['images'] = save_files(new_images, news_folder())
            else:
                del values['images']
            news_model.update(id, **values)
            return jsonify({'reload': True})
        set_values_to_form(form, news)
        return jsonify({'htmlresponse': render_template('modal_form.html', form=form, action=url_for('news.edit', id=id))})
    abort(403)


@news.route('/news/delete/<int:id>', methods=['POST'])
@admin_required
def delete(id):
    news = news_model.getone(id)
    if is_its_account(news['user_login']):
        delete_file(news['cover'], news_folder())
        delete_files(news['images'], news_folder())
        news_model.delete(id)
        return redirect(url_for('news.all'))
    abort(403)


@news.route('/comments/<int:id>', methods=['POST'])
def comments(id):
    comments = comments_model.appendone_getall(comments_model.getall({'key': 'posted_time', 'reverse': False}, news_id=id), users_model, ['user_login', 'login'])
    return jsonify({'htmlresponse': render_template('comments.html', comments=comments)})


@news.route('/comment/edit/<int:id>', methods=['POST'])
@login_required
def edit_comment(id):
    form = CreateCommentForm()
    comments = comments_model.getone(id)
    if is_its_account(comments['user_login']):
        if request.form.get('show'):
            pass
        elif form.validate_on_submit():
            values = get_values_from_form(form)
            comments_model.update(id, **values)
            return jsonify({'reload': True})
        set_values_to_form(form, comments)
        return jsonify({'htmlresponse': render_template('modal_form.html', form=form, action=url_for('news.edit_comment', id=id))})
    abort(403)


@news.route('/comment/delete/<int:id>', methods=['POST'])
@login_required
def delete_comment(id):
    comment = comments_model.getone(id)
    if is_its_account(comment['user_login']):
        comments_model.delete(id)
        return redirect(url_for('news.one', id=comment['news_id']))
    abort(403)


