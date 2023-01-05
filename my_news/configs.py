import secrets
from .instance.config import *


app_development = {'DEBUG': True,
                'UPLOAD_FOLDER': 'static/' + 'files/',
                'SECRET_KEY': secrets.token_hex(16)}


database_development = {'host': 'localhost',
                'database': 'news',
                **DATABASE_USER}
