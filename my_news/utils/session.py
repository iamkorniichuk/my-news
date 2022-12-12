from flask import session, abort
from ..models.users import users_model
from functools import wraps


def logged_user():
    if is_fresh_logged():
        return users_model.getone(session['user']['login'])


def is_its_account(login):
    if is_fresh_logged():
        return logged_user()['login'] == login
    return False


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return func(*args, **kwargs)
        else:
            abort(401)
    return wrapper


def fresh_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_fresh_logged():
            return func(*args, **kwargs)
        else:
            abort(401)
    return wrapper


def add_session_user(login):
    session.permanent = True
    session['user'] = users_model.getone(login)


def is_fresh_logged():
    if 'user' in session:
        user = session['user']
        login = user['login']
        password = user['password']
        user = users_model.getone(login)
        if user:
            return password == user['password']
    return False
