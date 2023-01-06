import json
from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from .forms import *
from my_news.utils.session import logged_user
from my_news.utils.files import replace_file, delete_file, users_folder
from my_news.utils.forms import set_values_to_form, get_values_from_form
import my_news.db.models as models
from my_news.utils.search import get_args


users = Blueprint('users', __name__)


@users.route('/getall', methods=['POST'])
def getall():
    fetched = models.users.search(*get_args(request.form, 'login', 'login'))
    if fetched:
        reverse = False
        order_by = 'news_count'

        values = request.form.get('search')
        if values:
            values = json.loads(values)
            if 'reverse' in values.keys():
                reverse = True if values['reverse'] == 'on' else False
            if 'search' in values.keys():
                if values['search']:
                    order_by = 'login'
        all_users = map(append_count, fetched)
        all_users = sorted(all_users, key=lambda d: d[order_by], reverse=not reverse) 

        return jsonify({'html': render_template('modules/users.html', users=all_users)})
    return  jsonify({'html': render_template('modules/error.html', message='No users yet')})


def append_count(user):
    user['news_count'] = models.news.count(user_login=user['login'])
    return user


@users.route('/get/<login>', methods=['POST'])
def getone(login):
    user = models.users.getone(login)
    return jsonify({'html': render_template('modules/user.html', user=user)})


@users.route('/edit', methods=['POST'])
@logged_user.login_required
def edit():
    form = EditAccountForm()
    if form.validate_on_submit():
        values = get_values_from_form(form)
        old_image = logged_user.info['image']
        new_image = values['image']
        values['image'] = replace_file(old_image, new_image, users_folder())
        if not values['image']:
            del values['image']
        models.users.update(logged_user.info['login'], **values)
        return jsonify({'status': True})
    set_values_to_form(form, logged_user.info)
    return jsonify({'html': render_template('modules/modal_form.html', form=form, action=url_for('users.edit'))})


@users.route('/delete', methods=['POST'])
@logged_user.login_required
def delete():
    if logged_user()['image']:
        delete_file(logged_user()['image'], users_folder())
    models.users.delete(logged_user()['login'])
    return redirect(url_for('auth.logout'), code=307)
