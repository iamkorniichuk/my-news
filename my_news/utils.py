from flask import session, redirect, url_for, current_app
from .models.users import users_model
from functools import wraps


def USERS_FOLDER():
    return url_for('static', filename='files/users/')


def POSTS_FOLDER():
    return url_for('static', filename='files/posts/')


def posts_file(name):
    if name:
        return POSTS_FOLDER() + name


def users_file(name):
    if name:
        return USERS_FOLDER() + name


def save_file(file, folder_func):
    file.save(current_app.root_path + folder_func() + file.filename)
    return file.filename


__logged_user = None


def logged_user():
    global __logged_user
    if is_logged():
        if not __logged_user:
            __logged_user = users_model.getone(session['user']['login'])
        return __logged_user


def is_logged_user(user):
    return logged_user()['login'] == user['login'] and logged_user()['password'] == user['password']


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
    return False
