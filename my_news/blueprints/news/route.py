from flask import Blueprint, render_template, request, url_for, abort, jsonify, json
from .forms import *
import my_news.db.models as models
from my_news.utils.session import logged_user
from my_news.utils.files import save_file, save_files, news_folder, delete_file, delete_files, replace_files, replace_file
from my_news.utils.forms import set_values_to_form, get_values_from_form
from my_news.utils.search import get_args


news = Blueprint('news', __name__)


@news.route('/get', methods=['POST'])
def getall():
    fetched = models.news.search(*get_args(request.form, 'title', 'posted_time'))
    if fetched:
        all_news = models.news.appendone_getall(fetched, models.users, ['user_login', 'login'])
        return jsonify({'html': render_template('modules/news_covers.html', news=all_news)})
    return jsonify({'html': render_template('modules/error.html', message='No news yet')})


@news.route('/get/<int:id>', methods=['POST'])
def getone(id):
    fetched = models.news.getone(id)
    all_news = models.news.appendone_getone(fetched, models.users, ['user_login', 'login'])
    if all_news['images']:
        all_news['images'].insert(0, all_news['cover'])
    else:
        all_news['images'] = None
    return jsonify({'html': render_template('modules/one_news.html', news=all_news)})


@news.route('/get/<login>', methods=['POST'])
def getusers(login):
    fetched = models.news.search(*get_args(request.form, 'title', 'posted_time'), user_login=login)
    if fetched:
        all_news = models.news.appendone_getall(fetched, models.users, ['user_login', 'login'])
        return jsonify({'html': render_template('modules/news_covers.html', news=all_news)})
    return jsonify({'html': render_template('modules/error.html', message='No news yet')})



@news.route('/add', methods=['POST'])
@logged_user.admin_required
def add():
    form = CreateNewsForm()
    if request.form.get('first_load'):
        pass
    elif form.validate_on_submit():
        values = get_values_from_form(form)
        values['user_login'] = logged_user.info['login']
        values['cover'] = save_file(values['cover'], news_folder())
        values['images'] = save_files(values['images'], news_folder())
        models.news.add(**values)
        return jsonify({'status': True})
    return jsonify({'html': render_template('modules/form.html', form=form, object='news_form')})


@news.route('/edit/<int:id>', methods=['POST'])
@logged_user.admin_required
def edit(id):
    form = EditNewsForm()
    one_news = models.news.getone(id)
    if logged_user.is_its_account(one_news['user_login']):
        if request.form.get('first_load'):
            pass
        elif form.validate_on_submit():
            values = get_values_from_form(form)
            old_cover = one_news['cover']
            new_cover = values['cover']
            values['cover'] = replace_file(old_cover,  new_cover, news_folder())
            if not values['cover']:
                del values['cover']
            old_images = one_news['images']
            new_images = values['images']
            values['images'] = replace_files(old_images,  new_images, news_folder())
            if not values['images']:
                del values['images']
            models.news.update(id, **values)
            return jsonify({'status': True})
        set_values_to_form(form, one_news)
        return jsonify({'html': render_template('modules/modal_form.html', form=form, action=url_for('news.edit', id=id))})
    abort(403)


@news.route('/delete/<int:id>', methods=['POST'])
@logged_user.admin_required
def delete(id):
    news = models.news.getone(id)
    if logged_user.is_its_account(news['user_login']):
        delete_file(news['cover'], news_folder())
        delete_files(news['images'], news_folder())
        models.news.delete(id)
        return jsonify({'status': True})
    return jsonify({'status': False})
