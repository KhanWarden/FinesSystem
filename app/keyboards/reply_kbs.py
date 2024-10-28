from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.database import AdminDatabase


def get_admins(db_path):
    admin_db = AdminDatabase(db_path)
    admins = admin_db.get_all_admins()
    return [admin['telegram_id'] for admin in admins]


def main_menu(user_telegram_id, db_path):
    admins = get_admins(db_path)

    kb_list = [
        [KeyboardButton(text='Мои штрафы'), KeyboardButton(text='')]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text='Админ Панель')])

    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, one_time_keyboard=True)
    return keyboard
