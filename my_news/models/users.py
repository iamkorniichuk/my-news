from .base import BaseModel
from hashlib import sha512
from my_news.utils.files import users_folder


class UsersModel(BaseModel):
    def __init__(self):
        super().__init__('users', 'login', folder=users_folder)
        

    def add(self, **kwargs):
        kwargs['password'] = self._hash(kwargs['password'])
        super().add(**kwargs)


    def _hash(self, str):
        return sha512(str.encode('utf-8')).hexdigest()


    def auth(self, login, password):
        user = self.getone(login)
        if user:
            return sha512(password.encode('utf-8')).hexdigest() == user['password']
        return False


users_model = UsersModel()
