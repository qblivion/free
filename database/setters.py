from .work_db import *
from . import keys


async def add_new_user(user_data):
    '''Добавление нового пользователя в базу данных'''
    query = '''
    INSERT INTO users
        {}
    VALUES
        ({});
    '''.format(
        str(keys.users),
        ', '.join(['?' for _ in keys.users])
    )
    await execute_query(query, user_data)