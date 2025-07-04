from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import mysql.connector

connection = mysql.connector.connect(host='127.0.0.1', user='root', password='Saf21Sls17Ssa07',
                                     database='base_for_keeper_bot')
cursor = connection.cursor()


# mm = main menu buttons
# sp = search by professor
# lwp = list of works by professor
# ss = search by subject
# stf = send this file
# lws = list of works by subject


def main_menu_buttons():
    inline_kb_list = [
        [InlineKeyboardButton(text="Искать работу по ФИО преподавателя", callback_data="sp")],
        [InlineKeyboardButton(text="Искать работу по предмету", callback_data="ss")],
        [InlineKeyboardButton(text="Что умеет бот?", callback_data="help")],
        [InlineKeyboardButton(text="Пожертвовать работу", callback_data="donate_work")],
        [InlineKeyboardButton(text="Поддержать автора копеечкой", callback_data="donate_money")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def mm_buttons():
    inline_kb_list = [
        [InlineKeyboardButton(text="Назад", callback_data="mm")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def list_of_professors():
    inline_kb_list = [[InlineKeyboardButton(text="Назад", callback_data="mm")]]
    cursor.execute("SELECT DISTINCT professor, p_id FROM professors_id ORDER BY professor ASC")
    result = cursor.fetchall()
    for i in result:
        inline_kb_list.append([InlineKeyboardButton(text=f"{i[0]}", callback_data="lwp" + f"{i[1]}")])
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def lwpessor(prof):
    inline_kb_list = [[InlineKeyboardButton(text="Назад", callback_data="sp")]]
    cursor.execute(f"SELECT work_name FROM done_works WHERE professor = "
                   f"(SELECT professor FROM professors_id WHERE p_id='{prof}') "
                   f"ORDER BY work_name ASC")
    result = cursor.fetchall()
    for i in result:
        inline_kb_list.append([InlineKeyboardButton(text=f"{i[0]}", callback_data="stf" + f'{i[0]}')])
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def list_of_subjects():
    # Получаем список предметов отсортированных по возрастанию. Колбэк к каждому в формате lwsПредмет
    inline_kb_list = [
        [InlineKeyboardButton(text="Назад", callback_data="mm")]
    ]
    cursor.execute("SELECT DISTINCT subject FROM done_works ORDER BY subject ASC")
    res = cursor.fetchall()
    for i in res:
        inline_kb_list.append([InlineKeyboardButton(text=f"{i[0]}", callback_data=f"lws{i[0]}")])
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def lwsect(subject):
    inline_kb_list = [
        [InlineKeyboardButton(text="Назад", callback_data="ss")]
    ]
    cursor.execute(f"SELECT work_name, work_number FROM done_works WHERE subject = '{subject}' ORDER BY work_name ASC")
    res = cursor.fetchall()
    for i in res:
        inline_kb_list.append([InlineKeyboardButton(text=i[0], callback_data="SeThFi"+str(i[1]))])
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
