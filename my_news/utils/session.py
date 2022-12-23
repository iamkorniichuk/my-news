from flask import session, abort
from ..models.users import users_model
from functools import wraps


def logged_user():
    if is_logged():
        return users_model.getone(session['user']['login'])


def is_its_account(login):
    if is_logged():
        try:
            return logged_user()['login'] == login
        except:
            delete_session_user()
    return False


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_logged():
            return func(*args, **kwargs)
        else:
            abort(401)
    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_admin():
            return func(*args, **kwargs)
        else:
            abort(403)
    return wrapper


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_logged():
            return func(*args, **kwargs)
        else:
            abort(401)
    return wrapper


def add_session_user(login):
    session.permanent = True
    session['user'] = users_model.getone(login)


def delete_session_user():
    session.pop('user', None)


# def fresh_login_required(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         if is_fresh_logged():
#             return func(*args, **kwargs)
#         else:
#             abort(401)
#     return wrapper


# def is_fresh_logged():
#     if 'user' in session:
#         user = session['user']
#         login = user['login']
#         password = user['password']
#         user = users_model.getone(login)
#         if user:
#             return password == user['password']
#     return False


def is_logged():
    return True if 'user' in session else False


def is_admin():
    if is_logged():
        user = users_model.getone(session['user']['login'])
        try:
            return user['is_admin']
        except:
            delete_session_user()
    return False
