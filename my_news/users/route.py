from flask import Blueprint, render_template, redirect, url_for
from .forms import *
from my_news.utils.session import login_required, logged_user, add_session_user
from my_news.utils.files import replace_file, delete_file,  users_folder
from my_news.utils.forms import set_values_to_form, get_values_from_form
from my_news.models.users import users_model
from my_news.models.posts import posts_model


users = Blueprint('users', __name__)


@users.route('/users')
def all():
    users = users_model.getallinorder({'key':'login', 'reverse':False})
    return render_template('users.html', title='News', users=users)


@users.route('/user/<login>')
def one(login):
    # TODO: To end
    user = users_model.getone(login)
    posts = posts_model.getallinorder({'key':'posted_time', 'reverse':False}, user_login=login)
    return render_template('user.html', title=user['login'], user=user, posts=posts)
    

@users.route('/account/')
@login_required
def me():
    user = logged_user()
    posts = posts_model.getallinorder({'key':'posted_time', 'reverse':False}, user_login=user['login'])
    return render_template('user.html', title=user['login'], user=user, posts=posts)
    

@users.route('/account/edit', methods=['POST', 'GET'])
@login_required
def edit():
    form = EditAccountForm()
    if form.validate_on_submit():
        values = get_values_from_form(form)
        old_image = logged_user()['image']
        new_image = values['image']
        values['image'] = replace_file(old_image, new_image, users_folder())
        # TODO: Refresh info in session | Will it be better if use caching?
        add_session_user(logged_user()['login'])
        users_model.update(logged_user()['login'], **values)
        return redirect(url_for('users.me'))
    set_values_to_form(form, logged_user())
    return render_template('edit_account.html', title='Edit Account', form=form)


@users.route('/account/delete', methods=['POST'])
@login_required
def delete():
    if logged_user()['image']:
        delete_file(logged_user()['image'], users_folder())
    users_model.delete(logged_user()['login'])
    return redirect(url_for('auth.logout'), code=307)
