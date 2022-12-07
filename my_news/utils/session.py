from flask import session, redirect, url_for
from ..models.users import users_model
from functools import wraps


def logged_user():
    global __logged_user
    if is_logged():
        return users_model.getone(session['user']['login'])


def is_its_account(login):
    if is_logged():
        return logged_user()['login'] == login
    return False


def login_required(func):
    @wraps(func)
    def wrapper():
        if is_logged():
            return func()
        else:
            return redirect(url_for('auth.login'))
    return wrapper


def add_session_user(login):
    session.permanent = True
    session['user'] = users_model.getone(login)


def is_logged():
    if 'user' in session:
        user = session['user']
        login = user['login']
        password = user['password']
        user = users_model.getone(login)
        if user:
            return password == user['password']
    return False
