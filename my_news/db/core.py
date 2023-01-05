import mysql.connector as mysql
from ..configs import database_development


__connect = mysql.connect(
     **database_development
     )
__cursor = __connect.cursor(dictionary=True, buffered=True)

def count(table, conditions_dict=None):
    query = f'SELECT COUNT(*) as count FROM {table}'
    if conditions_dict:
        conditions = __convert_to_conditions(conditions_dict)
        query += f' WHERE {conditions}'
    __executeone(query, commit=False)
    return __cursor.fetchall()[0]['count']


def selectlike(table, column, text, conditions_dict=None, order_dict=None):
    query = f'SELECT * FROM {table} WHERE '
    if conditions_dict:
        conditions = __convert_to_conditions(conditions_dict)
        query += f'{conditions} and '
    query+= f'{column} like {__value_quote(f"%{text}%")}'
    if order_dict:
        order = __convert_to_order(order_dict)
        query += f' ORDER BY {order}'
    __executeone(query, commit=False)
    return __cursor.fetchall()


def selectall(table, conditions_dict=None, order_dict=None):
    query = f'SELECT * FROM {table}'
    if conditions_dict:
        conditions = __convert_to_conditions(conditions_dict)
        query += f' WHERE {conditions}'
    if order_dict:
        order = __convert_to_order(order_dict)
        query += f' ORDER BY {order}'
    __executeone(query, commit=False)
    return __cursor.fetchall()


def selectallin(table, in_dict, order_dict=None):
    query = f'SELECT * FROM {table}'
    condition = __convert_to_in_condition(in_dict)
    query += f' WHERE {condition}'
    if order_dict:
        order = __convert_to_order(order_dict)
        query += f' ORDER BY {order}'
    __executeone(query, commit=False)
    return __cursor.fetchall()


def selectone(table, conditions_dict):
    query = f'SELECT * FROM {table}'
    conditions = __convert_to_conditions(conditions_dict)
    query += f' WHERE {conditions}'
    __executeone(query, commit=False)
    return __cursor.fetchone()


def insertone(table, columns_values_dict):
    columns, values = __convert_to_columns_values(columns_values_dict)
    __executeone(f'INSERT INTO {table} {columns} VALUES {values}')


def update(table, set_dict, conditions_dict):
    set = __convert_to_set(set_dict)
    conditions = __convert_to_conditions(conditions_dict)
    __executeone(f'UPDATE {table} SET {set} WHERE {conditions}')


def delete(table, conditions_dict):
    conditions = __convert_to_conditions(conditions_dict)
    __executeone(f'DELETE FROM {table} WHERE {conditions}')


def __executeone(query, commit=True):
    __cursor.reset()
    __cursor.execute(query)
    if commit: __connect.commit()


def __convert_to_order(dict):
    if 'key' in dict.keys():
        order_by_string = dict['key']
    else:
        order_by_list = []
        for key in dict['keys']:
            order_by_list.append(key)
        order_by_string = ', '.join(order_by_list)
    order = 'ASC' if dict['reverse'] else 'DESC'
    return order_by_string + ' ' + order


def __convert_to_set(dict):
    list = []
    for key, value in dict.items():
        list.append(f'{key} = {__value_quote(value)}')
    return ', '.join(list)


def __convert_to_in_condition(dict):
    list = []
    for key, value in dict.items():
        list.append(f'{key} in {__set_bracket(", ".join(value))}')
    return ' and '.join(list)


def __convert_to_conditions(dict):
    list = []
    for key, value in dict.items():
        list.append(f'{key} = {__value_quote(value)}')
    return ' and '.join(list)


def __convert_to_columns_values(dict):
    columns_list = list(dict.keys())
    columns_string = ', '.join(columns_list)
    values_list =list(map(__value_quote, dict.values()))
    values_string = ', '.join(values_list)
    return __set_bracket(columns_string), __set_bracket(values_string)


def __set_bracket(str):
    return f'({str})'


def __value_quote(str):
    return f'"{str}"'
