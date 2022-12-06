from flask import url_for, current_app


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