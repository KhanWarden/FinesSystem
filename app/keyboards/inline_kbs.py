from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def game_counter(buttons_data):
    if not buttons_data:
        raise ValueError("Кнопки не могут быть пустыми.")

    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data=button_id)]
        for button_id, text in buttons_data.items()
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
