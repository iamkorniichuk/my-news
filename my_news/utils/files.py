from flask import url_for, current_app
from glob import glob
import os
import secrets


def users_folder(file=None):
    name = 'files/users/'
    if file:
        name += file
    return url_for('static', filename=name)


def posts_folder(file=None):
    name = 'files/posts/'
    if file:
        name += file
    return url_for('static', filename=name)


def save_file(file, folder):
    name = get_unique_filename(folder)
    file.save(current_app.root_path + folder + name)
    return name


def delete_file(file, folder):
    path = current_app.root_path + folder + file
    if os.path.exists(path) and file:
        os.chmod(path, 0o777)
        os.remove(path)


def get_unique_filename(folder):
    name = secrets.token_hex(16)
    while os.path.exists(folder + name):
        name = secrets.token_hex(16)
    return name
