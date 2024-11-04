from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def certificates_kb():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Создать новый", callback_data="create_new_cert")],
        [InlineKeyboardButton(text="🔍 Проверить сертификат", callback_data="check_cert")],
        [InlineKeyboardButton(text="↩️ Вернуться в главное меню", callback_data="to_main_menu")]
    ])
    return inline_kb


def certificates_sum_kb():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="5.000 ₸", callback_data='cert_5k'),
         InlineKeyboardButton(text="10.000 ₸", callback_data='cert_10k')],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data='back_to_cert_menu')]
    ])
    return inline_kb


def certificate_date_for_5k_kb():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Текущая дата", callback_data='current_date_for_5k'),
         InlineKeyboardButton(text="🖊 Ввести свою дату", callback_data='date_from_user_for_5k')],
        [InlineKeyboardButton(text="↩️ В главное меню", callback_data='to_main_menu')]
    ])
    return inline_kb


def certificate_date_for_10k_kb():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Текущая дата", callback_data='current_date_for_10k'),
         InlineKeyboardButton(text="Ввести свою дату", callback_data='date_from_user_for_10k')]
    ])
    return inline_kb
