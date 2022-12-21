import os
from .instance.config import *

# TODO: Secure SECRET_KEY
app_development = {'DEBUG': True,
                'UPLOAD_FOLDER': os.path.join('static/' + 'files/'),
                'SECRET_KEY': 'ha'}


database_development = {'host': 'localhost',
                'database': 'news',
                **DATABASE_USER}
