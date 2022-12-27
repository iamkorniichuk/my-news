from flask import Blueprint, render_template, redirect, url_for, request, jsonify, abort
from my_news.models.reviews import reviews_model
from .forms import *
from my_news.utils.forms import set_values_to_form, get_values_from_form
from my_news.utils.session import login_required, logged_user, is_its_account
from my_news.utils.files import users_folder


about = Blueprint('about', __name__)


@about.route('/about', methods=['POST', 'GET'])
@about.route('/reviews', methods=['POST', 'GET'])
def info():
    form = CreateReviewForm()
    if form.validate_on_submit():
        values = get_values_from_form(form)
        if reviews_model.getone(logged_user()['login']):
            reviews_model.update(logged_user()['login'], **values)
        else:
            values['user_login'] = logged_user()['login']
            reviews_model.add(**values)
        return redirect(url_for('about.info'))
    fetched = reviews_model.search('body', request.args.get('search'), {'key':'stars', 'reverse':True})
    reviews = reviews_model.appendone_getall(fetched, 'users', ['user_login', 'login'])
    return render_template('about.html', title='About', reviews=reviews, form=form)


@about.route('/review/edit/<string:login>', methods=['POST'])
@login_required
def edit_review(login):
    form = CreateReviewForm()
    review = reviews_model.getone(login)
    if is_its_account(review['user_login']):
        if request.form.get('show'):
            pass
        elif form.validate_on_submit():
            values = get_values_from_form(form)
            reviews_model.update(login, **values)
            return jsonify({'reload': True})
        set_values_to_form(form, review, users_folder)
        return jsonify({'htmlresponse': render_template('modal_form.html', form=form, action=url_for('about.edit_review', login=login))})
    abort(403)


@about.route('/review/delete/<string:login>', methods=['POST'])
@login_required
def delete_review(login):
    review = reviews_model.getone(login)
    if is_its_account(review['user_login']):
        reviews_model.delete(login)
        return redirect(url_for('about.info'))
    abort(403)
