from .work_db import *
from . import keys


async def get_user_data(user_id):
    '''Возвращает информацию о пользователе'''
    query = '''
    SELECT
        *
    FROM
        users
    WHERE
        user_id = ?
    '''

    users_data = await execute_query(query, [user_id], fetch='one')

    if users_data:
        return dict(zip(keys.users, users_data[0]))