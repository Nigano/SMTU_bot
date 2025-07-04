import asyncio

import aiogram
from aiogram import Bot, types
from aiogram.filters import CommandStart
from all_buttons import *
import mysql.connector

BOT_TOKEN = input("Gimme token: ")
bot = Bot(token=BOT_TOKEN)
dp = aiogram.Dispatcher()

connection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='Saf21Sls17Ssa07',
    database='base_for_keeper_bot'
)
cursor = connection.cursor()


# mm = main menu buttons
# sp = search by professor
# lwp = list of works by professor
# ss = search by subject
# stf = send this file


@dp.callback_query(lambda c: c.data == "help")
async def process_callback_help_button(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, text="Этот бот хранит многие работы, выполненные студентами "
                                                             "нашего ВУЗа. Доступно два варианта поиска интересующей "
                                                             "тебя работы: поиск по преподавателю и поиск по предмету "
                                                             "(p.s. Работы, для которых нам не удалось установить "
                                                             "преподавателя находятся в разделе <Искать работу по "
                                                             "фио> -> <Неизвестно>)", reply_markup=mm_buttons())
    await callback_query.answer()


@dp.callback_query(lambda c: c.data == "mm")
async def process_callback_mm_button(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, text="Привет, студент! Какую работу ищешь?",
                           reply_markup=main_menu_buttons())
    await callback_query.answer()


@dp.callback_query(lambda c: c.data == "sp")
async def process_callback_list_of_professors(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, text="Вот список преподавателей, чьи работы у нас есть:",
                           reply_markup=list_of_professors())
    await callback_query.answer()


@dp.callback_query(lambda c: "lwp" in c.data)
async def lwp(callback_query: types.CallbackQuery):
    prof = callback_query
    prof = prof.data
    prof = prof.split("lwp")[1]
    answ = lwpessor(prof)
    cursor.execute(f"SELECT professor FROM professors_id WHERE p_id = {prof}")
    professors = cursor.fetchall()
    professors = professors[0][0]
    await bot.send_message(callback_query.from_user.id,
                           text=f"Вот список работ, которые у нас есть по преподавателю {professors}",
                           reply_markup=answ)
    await callback_query.answer()


@dp.callback_query(lambda c: "lws" in c.data)
async def process_callback_lws(callback_query: types.CallbackQuery):
    subject = callback_query
    subject = subject.data
    subject = subject.split("lws")[1]
    answ = lwsect(subject)
    await bot.send_message(callback_query.from_user.id, text=f"Вот список работ, которые у нас есть по предмету "
                                                             f"{subject}", reply_markup=answ)
    await callback_query.answer()


@dp.callback_query(lambda c: c.data == "ss")
async def process_callback_list_of_subjects(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, text="Вот список предметов, по которым у нас есть работы:",
                           reply_markup=list_of_subjects())
    await callback_query.answer()


@dp.callback_query(lambda c: "stf" in c.data)
async def process_callback_send_this_file(callback_query: types.callback_query.CallbackQuery):
    document_name = callback_query
    document_name = document_name.data
    document_name = document_name.split("stf")[1]
    cursor.execute(f"SELECT tg_file_id FROM done_works WHERE work_name = '{document_name}'")
    send_file = cursor.fetchall()
    await bot.send_document(chat_id=callback_query.from_user.id, document=send_file[0][0],
                            reply_markup=mm_buttons())
    await callback_query.answer()


@dp.callback_query(lambda c: "SeThFi" in c.data)
async def process_callback_SEND_THIS_FILE(callback_query: types.CallbackQuery):
    doc_id = callback_query
    doc_id = doc_id.data
    doc_id = doc_id.split("SeThFi")[1]
    cursor.execute(f"SELECT tg_file_id FROM done_works WHERE work_number = '{doc_id}'")
    send_file = cursor.fetchall()
    await bot.send_document(chat_id=callback_query.from_user.id, document=send_file[0][0], reply_markup=mm_buttons())
    await callback_query.answer()


@dp.callback_query(lambda c: c.data == "donate_money")
async def donate_money(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, text="Этот проект стал для меня возможностью упростить жизнь "
                                                             "таким же, как и я, студентам. Делал я его не "
                                                             "рассчитывая на какую-либо прибыль. Если у вас появится "
                                                             "желание поделиться своими кровными, буду безмерно "
                                                             "благодарен! \n\n Сбор в Т-Банке: "
                                                             "https://www.tbank.ru/cf/7XYDYEgKt0V",
                           reply_markup=mm_buttons())
    await callback_query.answer()


@dp.callback_query(lambda c: c.data == "donate_work")
async def donate_work(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, text="Отправить свою готовую работу можно на электронную почту"
                                                             " нашего бота: \n\n keeper_bot@mail.ru \n\nПожалуйта, не "
                                                             "забудь указать предмети преподавателя! Спасибо за вклад в"
                                                             " развитие проекта!", reply_markup=mm_buttons())
    await callback_query.answer()


@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer("Привет, студент! Какую работу ищешь?",
                         reply_markup=main_menu_buttons())


async def main():
    try:
        print('Работаем, босс!')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        print("Сессия бота закрыта")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен пользователем")
