from .base import BaseModel
from hashlib import sha512


class UsersModel(BaseModel):
    def __init__(self):
        super().__init__('users', 'login')


    def add(self, **kwargs):
        kwargs['password'] = self._hash(kwargs['password'])
        super().add(**kwargs)


    def _hash(self, str):
        return sha512(str.encode('utf-8')).hexdigest()


    def auth(self, login, password):
        user = self.getone(login)
        return sha512(password.encode('utf-8')).hexdigest() == user[password]


users_model = UsersModel()
