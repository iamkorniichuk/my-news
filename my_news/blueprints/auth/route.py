from flask import Blueprint, render_template, redirect, url_for
from .forms import *
import my_news.db.models as models
from my_news.utils.session import logged_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        if models.users.auth(login, password):
            logged_user.info = login
            return redirect(url_for('pages.news'))
            # TODO: Render through ajax?
    return render_template('pages/auth.html', title='Log In', form=form)


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        login = form.login.data
        password = form.password.data
        models.users.add(email=email, login=login, password=password)
        logged_user.info = login
        return redirect(url_for('pages.news'))
    return render_template('pages/auth.html', title='Sign Up', form=form)


@auth.route('/logout', methods=['POST', 'GET'])
@logged_user.login_required
def logout():
    del logged_user.info
    return redirect(url_for('auth.login'))
