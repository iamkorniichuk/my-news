from flask import Blueprint, render_template, redirect, url_for
from my_news.models.reviews import reviews_model
from .forms import *
from my_news.utils.forms import set_values_to_form, get_values_from_form
from my_news.utils.session import login_required, logged_user, is_its_account


about = Blueprint('about', __name__)


@about.route('/about')
@about.route('/reviews')
def info():
    allreviews = reviews_model.getall({'key':'stars', 'reverse':True})
    return render_template('about.html', title='About', reviews=allreviews)


@about.route('/review/create', methods=['POST', 'GET'])
@about.route('/review/edit', methods=['POST', 'GET'])
@login_required
def create():
    form = CreateReviewForm()
    review = reviews_model.getone(logged_user()['login'])
    if form.validate_on_submit():
        values = get_values_from_form(form)
        values['user_login'] = logged_user()['login']
        if review:
            reviews_model.update(logged_user()['login'], **values)
        else:
            reviews_model.add(**values)
        return redirect(url_for('about.info'))
    set_values_to_form(form, review)
    # TODO: Refactor - unite all create/edit to one template
    return render_template('create_news.html', title='Create', form=form)
    