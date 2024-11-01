from aiogram.filters import callback_data
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.database import is_admin


def main_kb(telegram_id):
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📄 Печать Сертификатов", callback_data='certificates'),
         InlineKeyboardButton(text="Штрафы", callback_data='penalties')],

        [InlineKeyboardButton(text="Калькулятор", callback_data='count')]
    ])
    if is_admin(telegram_id):
        inline_kb.append([InlineKeyboardButton(text="Админ панель")])
    return inline_kb


def admin_panel_kb():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить админа", callback_data='add_admin'),
         InlineKeyboardButton(text="Удалить админа", callback_data='remove_admin')],
        [InlineKeyboardButton(text="Сертификаты", callback_data='certificate')]
    ])


def game_counter(buttons_data):
    if not buttons_data:
        raise ValueError("Кнопки не могут быть пустыми.")

    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data=button_id)]
        for button_id, text in buttons_data.items()
    ])
    return inline_kb


# TODO: optimize inline_kb
def game_counter_(tmp):
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"👥 Количество участников {tmp}", callback_data="button_guests_amount")]

    ])
    return inline_kb


def prepayment_button():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="5.000", callback_data='button_5000'),
         InlineKeyboardButton(text="25.000", callback_data='button_25000')],
    ])
    return inline_kb


def return_button():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='return')],
    ])
    return inline_kb


def certificates_kb():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Создать новый", callback_data="create_new_cert"),
         InlineKeyboardButton(text="🔍 Проверить сертификат", callback_data="check_cert")],
        [InlineKeyboardButton(text="↩️ Вернуться в главное меню", callback_data="to_main_menu")]
    ])
    return inline_kb
