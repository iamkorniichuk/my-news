from flask import Blueprint, render_template, session, redirect, url_for
from .forms import *
from my_news.models.users import users_model
from my_news.utils.session import add_session_user, delete_session_user, login_required


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        if users_model.auth(login, password):
            add_session_user(login)
            return redirect(url_for('news.all'))
    return render_template('login.html', title='Log In', form=form)


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        login = form.login.data
        password = form.password.data
        users_model.add(email=email, login=login, password=password)
        add_session_user(login)
        return redirect(url_for('news.all'))
    return render_template('signup.html', title='Sign Up', form=form)


@auth.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    # TODO: Clear localStorage when logout
    delete_session_user()
    return redirect(url_for('auth.login'))