import sqlite3


DB_PATH = 'database/database.sqlite'


async def get_connect(db_name=DB_PATH):
    '''Возвращает подключение к БД'''
    return sqlite3.connect(db_name)


async def execute_query(query, params=None, fetch=False, db_name=DB_PATH):
    '''Отправляет запрос к БД'''
    connect = await get_connect(db_name)
    cursor = connect.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    if fetch == 'one':
        return cursor.fetchone()
    elif fetch == 'all':
        return cursor.fetchall()

    connect.commit()
    connect.close()


async def create_tables():
    '''Создание таблиц в БД'''
    users = '''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name_user TEXT
    );
    '''

    await execute_query(users)