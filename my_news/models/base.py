from my_news import database


class BaseModel:
    def __init__(self, table, id):
        self._table = table
        self._id = id


    def getall(self, order=None, **kwargs):
        return database.selectall(self._table, kwargs, order)


    def getallin(self, in_dict, order=None):
         return database.selectallin(self._table, in_dict, order)


    def getone(self, id):
        return database.selectone(self._table, {self._id: id})


    def add(self, **kwargs):
        database.insertone(self._table, kwargs)


    def update(self, id, **kwargs):
        database.update(self._table, kwargs, {self._id: id})


    def delete(self, id):
        database.delete(self._table, {self._id: id})


    def exists(self, value, key=None):
        if not key:
            key = self._id
        return True if database.selectone(self._table, {key: value}) else False
