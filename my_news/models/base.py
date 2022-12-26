from my_news import database


class BaseModel:
    def __init__(self, table, id):
        self.table = table
        self.id = id


    def appendone_getall(self, fetched, table, linked_keys):
        for i in range(len(fetched)):
            fetched[i] = self.appendone_getone(fetched[i], table, linked_keys)
        return fetched


    def appendone_getone(self, fetched, table, linked_keys):
        return database.selectone(table, {linked_keys[1]: fetched[linked_keys[0]]}) | fetched


    def getall(self, order=None, **kwargs):
        return database.selectall(self.table, kwargs, order)


    def getallin(self, in_dict, order=None):
        return database.selectallin(self.table, in_dict, order)


    def getone(self, id):
        return database.selectone(self.table, {self.id: id})


    def search(self, key, text, order=None):
        if text:
            return database.selectlike(self.table, key, text, order)
        return self.getall(order)


    def count(self, **kwargs):
        return database.count(self.table, kwargs)


    def add(self, **kwargs):
        # TODO: INSERT QUOTES IN
        database.insertone(self.table, kwargs)


    def update(self, id, **kwargs):
        database.update(self.table, kwargs, {self.id: id})


    def delete(self, id):
        database.delete(self.table, {self.id: id})


    def exists(self, value, key=None):
        if not key:
            key = self.id
        return True if database.selectone(self.table, {key: value}) else False
