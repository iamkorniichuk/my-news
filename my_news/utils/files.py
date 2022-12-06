from flask import url_for, current_app
from glob import glob
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


def get_unique_filename(folder):
    pathes = glob(folder)
    filenames = []
    for path in pathes:
        filenames.append(path[path.rindex('/'):])
    print(filenames)
    name = secrets.token_hex(16)
    while name in filenames:
        name = secrets.token_hex(16)
    print(name)
    return name
