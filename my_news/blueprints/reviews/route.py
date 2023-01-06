import json
from flask import Blueprint, render_template, request, jsonify
from my_news.utils.session import logged_user
from my_news.utils.forms import set_values_to_form, get_values_from_form
import my_news.db.models as models
from .forms import *
from my_news.utils.search import get_args


reviews = Blueprint('reviews', __name__)


@reviews.route('/getall', methods=['POST'])
def getall():
    fetched = models.reviews.search(*get_args(request.form, 'body', 'stars'))
    if fetched:
        reverse = False
        order_by = 'stars'

        values = request.form.get('search')
        if values:
            values = json.loads(values)
            if 'reverse' in values.keys():
                reverse = True if values['reverse'] == 'on' else False
            if 'search' in values.keys():
                if values['search']:
                    order_by = 'body'
        all_reviews = sorted(fetched, key=lambda d: d[order_by], reverse=reverse) 

        all_reviews = models.reviews.appendone_getall(fetched, models.users, ['user_login', 'login'])
        return jsonify({'html': render_template('modules/reviews.html', reviews=all_reviews)})
    return jsonify({'html': render_template('modules/error.html', message='No reviews yet')})


@reviews.route('/add', methods=['POST'])
@logged_user.login_required
def add():
    form = CreateReviewForm()
    login = logged_user.info['login']
    review = models.reviews.getone(login)
    if request.form.get('first_load'):
        pass
    elif form.validate_on_submit():
        values = get_values_from_form(form)
        if review:
            models.reviews.update(login, **values)
        else:
            values['user_login'] = logged_user.info['login']
            models.reviews.add(**values)
        review = models.reviews.getone(login)
        set_values_to_form(form, review)
        return jsonify({'status': True, 'html': render_template('modules/form.html', form=form, object='reviews_form')})
    return jsonify({'html': render_template('modules/form.html', form=form, object='reviews_form')})


@reviews.route('/edit', methods=['POST'])
@logged_user.login_required
def edit():
    form = CreateReviewForm()
    login = logged_user.info['login']
    review = models.reviews.getone(login)
    if request.form.get('first_load'):
        pass
    elif form.validate_on_submit():
        values = get_values_from_form(form)
        models.reviews.update(login, **values)
        return jsonify({'status': True})
    set_values_to_form(form, review)
    return jsonify({'html': render_template('modules/modal_form.html', form=form)})


@reviews.route('/delete', methods=['POST'])
@logged_user.login_required
def delete():
    login = logged_user.info['login']
    review = models.reviews.getone(login)
    if review:
        models.reviews.delete(login)
        return jsonify({'status': True})
    return jsonify({'status': False})

    