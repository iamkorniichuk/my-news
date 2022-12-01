from flask import session, redirect, url_for
from .models.users import users_model
from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper():
        if is_logged():
            return func()
        else:
            return redirect(url_for('auth.login'))
    return wrapper


def add_session_user(login, password):
    session.permanent = True
    session['user'] = {'login': login, 'password': password}


def is_logged():
    if 'user' in session:
        user = session['user']
        login = user['login']
        password = user['password']
        return users_model.auth(login, password)
    else:
        return False
