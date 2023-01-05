from flask import request, json


def get_args(form, key, ordering):
    reverse = False
    search = None
    order_by = ordering

    values = form.get('search')
    values = json.loads(values)
    if 'reverse' in values.keys():
        reverse = True if values['reverse'] == 'on' else False
    if 'search' in values.keys():
        if values['search']:
            search = values['search']
            order_by = key
    return [key, search, {'key': order_by, 'reverse': reverse}]