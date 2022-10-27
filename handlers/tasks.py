import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.builtin import Command

from loader import dp
from tasks.tasks import TASKS


async def get_msg_text_question(block, qN):
    '''Возвращает сообщение для вопроса'''
    question = TASKS[block][qN]
    n_block = block.split('_')[-1]
    n_question = [i for i in qN][-1]
    msg_text = (
        f'БЛОК {n_block}\n' + f'№{n_question}. {question["question"]}' + '\n\n'
    )

    for number, answer in question['answer_options'].items():
        msg_text += f'{number}) {answer}\n'

    return msg_text


async def get_keyboard_select_answer(block, qN):
    '''Возвращает клавиатуру для выбора ответа'''
    number_block = block.split('_')[-1]
    number_question = [i for i in qN][-1]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    answers = TASKS[block][qN]['answer_options']
    right_answer = TASKS[block][qN]['right_answer']
    buttons = []

    for number in answers.keys():
        callback_data = (f'answer_right_{number_block}_{number_question}'
                         if number == right_answer
                         else f'answer_wrong_{number_block}_{number_question}')
        buttons.append(
            types.InlineKeyboardButton(number, callback_data=callback_data)
        )

    keyboard.add(*buttons)

    return keyboard


@dp.callback_query_handler(Text('start_tasks'))
@dp.message_handler(Command('tasks'))
async def start_tasks(call: types.CallbackQuery,
                      state: FSMContext):
    '''Запуск блока с заданиями'''
    if 'data' in call:
        await call.answer()

    block, qN = 'block_1', 'q1'
    msg_text = await get_msg_text_question(block, qN)
    keyboard = await get_keyboard_select_answer(block, qN)

    if 'data' in call:
        message_data = await call.message.answer(msg_text,
            reply_markup=keyboard)
    else:
        message = call
        message_data = await message.answer(msg_text, reply_markup=keyboard)

    await state.update_data(last_msg_ids=[message_data.message_id])


@dp.callback_query_handler(Text(startswith='answer_'))
async def next_question(call: types.CallbackQuery, state: FSMContext):
    '''Следующий вопрос'''
    print(call.data)
    last_msg_ids = []
    type_answer, n_block, n_question  = call.data.split('_')[1:]
    block, qN = f'block_{n_block}', f'q{n_question}'
    end_tasks_msg = (
        'Поздравляем! Вы завершили чат-бот «Когнитивные искажения в '
        'коммуникации». Вы сможете вернуться к нему в любой момент и '
        'пройти заново. Для этого напишите команду /tasks.'
    )

    if type_answer == 'right':
        await call.answer()
        info_right_answer = (
            '<b>Верно! ✅</b>'
        )
        await call.message.answer(info_right_answer)

        if n_block == '5' and n_question == '4':
            await call.message.answer(end_tasks_msg)
    else:
        await call.answer('Неправильно! ❌')
        comment = TASKS[block][qN].get('comment', None)
        right_answer = TASKS[block][qN]['answer_options'][
            TASKS[block][qN]['right_answer']]
        info_right_answer = (
            f'<b>Правильный ответ:</b> <i>{right_answer}</i>\n\n'
        )

        if comment:
            info_right_answer += f'{comment}'

        message_data = await call.message.answer(info_right_answer)
        last_msg_ids.append(message_data.message_id)

        if n_block == '5' and n_question == '4':
            await call.message.answer(end_tasks_msg)

    # Следующий блок и/или вопрос
    if not TASKS[block].get(f'q{int(n_question) + 1}', None):
        block = f'block_{int(n_block) + 1}'
        qN = f'q1'
    else:
        qN = f'q{int(n_question) + 1}'

    msg_text = await get_msg_text_question(block, qN)
    keyboard = await get_keyboard_select_answer(block, qN)

    # Удаление клавиатуры у предыдущих сообщений
    state_data = await state.get_data()

    for last_msg_id in state_data['last_msg_ids']:
        try:
            await dp.bot.edit_message_reply_markup(call.from_user.id,
                last_msg_id, reply_markup=None)
        except:
            pass

    if n_block == '1' and n_question == '2':
        message_data = await call.message.answer_video(open('b1q3.mp4',
            'rb'), caption=msg_text, reply_markup=keyboard)
    else:
        message_data = await call.message.answer(msg_text,
            reply_markup=keyboard)

    last_msg_ids.append(message_data.message_id)
    await state.update_data(last_msg_ids=last_msg_ids)
