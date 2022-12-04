import os
from .instance.config import *


class App:
    development = {'DEBUG': True,
                'UPLOAD_FOLDER': os.path.join('static/' + 'files/'),
                'SECRET_KEY': 'ha'}


class Database:
    development = {'host': 'localhost',
                'database': 'my_news',
                **DATABASE_USER}

