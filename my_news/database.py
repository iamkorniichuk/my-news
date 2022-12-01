import mysql.connector as mysql


__connect = mysql.connect(
     host='localhost',
     database='my_news',
     user='root',
     password=''
     )
__cursor = __connect.cursor(dictionary=True)


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


def selectone(table, conditions_dict):
    conditions = __convert_to_conditions(conditions_dict)
    __executeone(f'SELECT * FROM {table} WHERE {conditions}', commit=False)
    return __cursor.fetchone()


def insertone(table, columns_values_dict):
    columns, values = __convert_to_columns_values(columns_values_dict)
    __executeone(f'INSERT INTO {table} ({columns}) VALUES ({values})')


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


# def _executemany(query):
#     __cursor.reset()
#     __cursor.executemany(query)
#     __connect.commit()

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
        list.append(f'{__column_quote(key)} = {__value_quote(value)}')
    return ', '.join(list)


def __convert_to_conditions(dict):
    list = []
    for key, value in dict.items():
        list.append(f'{__column_quote(key)} = {__value_quote(value)}')
    return ', '.join(list)


def __convert_to_columns_values(dict):
    columns_list = list(map(__column_quote, dict.keys()))
    columns_string = ', '.join(columns_list)
    values_list =list(map(__value_quote, dict.values()))
    values_string = ', '.join(values_list)
    return __set_bracket(columns_string), __set_bracket(values_string)


def __set_bracket(str):
    return '(' + str + ')'


def __column_quote(str):
    return '`' + str + '`'


def __value_quote(str):
    return '"' + str + '"'
