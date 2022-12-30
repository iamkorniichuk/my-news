from my_news import database
from functools import wraps


class BaseModel:
    def __init__(self, table, id, folder = None):
        self.table = table
        self.id = id
        self.folder = folder


    def convert_filenames_to_path(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            fetched = func(self, *args, **kwargs)
            if isinstance(fetched, dict):
                fetched = self.convert_filenames_in_dict(fetched)
            elif isinstance(fetched, list):
                for row in fetched:
                    row = self.convert_filenames_in_dict(row)
            return fetched
        return wrapper


    def convert_filenames_in_dict(self, dict):
        keys_to_convert = ['image', 'images', 'cover']
        for key in keys_to_convert:
            try:
                if not dict[key].startswith('/'):
                    if key == 'images':
                        if dict[key]:
                            dict[key] = dict[key].split(' ')
                            for i in range(len(dict[key])):
                                dict[key][i] = self.folder(dict[key][i])
                    else:
                        dict[key] = self.folder(dict[key])
            except:
                continue
        return dict


    def appendone_getall(self, fetched, model, linked_keys):
        for i in range(len(fetched)):
            fetched[i] = self.appendone_getone(fetched[i], model, linked_keys)
        return fetched


    def appendone_getone(self, fetched, model, linked_keys):
        try:
            kwargs = {linked_keys[1]: fetched[linked_keys[0]]}
            result = model.getall(**kwargs)[0] | fetched
        except:
            result = fetched
        return result


    @convert_filenames_to_path
    def getall(self, order=None, **kwargs):
        return database.selectall(self.table, kwargs, order)


    @convert_filenames_to_path
    def getallin(self, in_dict, order=None):
        return database.selectallin(self.table, in_dict, order)


    @convert_filenames_to_path
    def getone(self, id):
        return database.selectone(self.table, {self.id: id})


    @convert_filenames_to_path
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
