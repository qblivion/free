import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp
from database import getters, setters


class StartStates(StatesGroup):
    waiting_for_name = State()


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    '''Запуск бота'''
    msg_text = (
        'Здравствуйте!\n\n'
        'На связи Ваш виртуальный помощник. Вашему вниманию будет '
        'предложена тема для отработки: «Когнитивные искажения». В процессе обучения Вам будут предложены '
        'различные задания. Ваша задача - выбрать правильный ответ.\n\n'
        'Перед началом, пожалуйста, ознакомьтесь с коротким видеороликом '
        'о том, как работать с ботом. Это не займет много времени.'
    )
    await message.answer(msg_text)
    await asyncio.sleep(3)
    await message.answer_video(open('video.mp4', 'rb'))

    users_data = await getters.get_user_data(message.from_user.id)

    if not users_data:
        await asyncio.sleep(100)

        msg_text = (
            'Теперь давайте познакомимся. Как Вас зовут?'
        )
        await message.answer(msg_text)
        await StartStates.waiting_for_name.set()


@dp.message_handler(state=StartStates.waiting_for_name)
async def add_new_user(message: types.Message, state: FSMContext):
    '''Добавление нового пользователя в базу данных'''
    await state.reset_state()
    name_user = message.text
    msg_text = (
        f'Приятно познакомиться, {name_user}!\n\n'
        'Наша тренировка рассчитана на 10 блоков.\n\n'
        '<i><b>Хочу еще раз Вас попросить использовать в тестовых заданиях '
        'кнопки и присылать мне текст только в случае открытого вопроса. '
        'Спасибо за понимание!</b></i>\n\n'
        'Готовы?😊'
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton('Поехали! 🚀', callback_data='start_tasks')
    )
    await message.answer(msg_text, reply_markup=keyboard)

    user_data = (
        message.from_user.id,
        name_user,
    )
    await setters.add_new_user(user_data)