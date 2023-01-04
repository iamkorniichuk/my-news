from flask import session, abort, redirect, url_for
import my_news.db.models as models
from functools import wraps


class LoggedUser:
    def __bool__(self):
        return True if 'user' in session else False


    def __get_info(self):
        if self:
            return models.users.getone(session['user']['login'])


    def __set_info(self, login):
        session.permanent = True
        session['user'] = models.users.getone(login)


    def __del_info(self):
        session.pop('user', None)


    info = property(__get_info, __set_info, __del_info)


    def login_required(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self:
                return func(*args, **kwargs)
            else:
                abort(401)
        return wrapper


    def __get_is_fresh_logged(self):
        if self:
            login = self.info['login']
            password = self.info['password']
            return models.users.auth(login, password)
        return False


    is_fresh_logged = property(__get_is_fresh_logged)


    def fresh_login_required(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.is_fresh_logged:
                return func(*args, **kwargs)
            else:
                abort(401)
        return wrapper


    def __get_is_admin(self):
        if self:
            try:
                row = models.users.getone(self.info['login'])
                return row['is_admin']
            except:
                return redirect(url_for('auth.logout'))
        return False


    is_admin = property(__get_is_admin)


    def admin_required(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.is_admin:
                return func(*args, **kwargs)
            else:
                abort(403)
        return wrapper


    def is_its_account(self, login):
        try:
            return login == self.info['login']
        except TypeError:
            return False


logged_user = LoggedUser()
