from aiogram import executor

import utils, handlers
from database import work_db
from loader import dp


async def on_startup(dp):
    '''Действия при запуске бота'''
    print('Бот запущен!')

    # Создание БД и таблиц в ней
    await work_db.create_tables()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)