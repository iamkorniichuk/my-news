from flask import Blueprint, render_template, redirect, url_for, request, jsonify, abort
from my_news.utils.session import logged_user
from my_news.utils.forms import set_values_to_form, get_values_from_form
import my_news.db.models as models
from my_news.utils.files import users_folder
from .forms import *


reviews = Blueprint('reviews', __name__)


@reviews.route('/getall', methods=['POST'])
def getall():
    fetched = models.reviews.getall({'key':'stars', 'reverse': False})
    if fetched:
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

    