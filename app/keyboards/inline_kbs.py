from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

prices = {
    "1_hour": {
        "fix": 100000,
        "16-25": 6000,
        "26-34": 5500,
        "35": 4500
    },
    "1.5_hours": {
        "fix": 150000,
        "16-25": 9000,
        "26-34": 8250,
        "35": 6750
    },
    "2_hours": {
        "fix": 200000,
        "16-25": 12000,
        "26-34": 11000,
        "35": 9000
    }
}


def game_counter(buttons_data):
    if not buttons_data:
        raise ValueError("Кнопки не могут быть пустыми.")

    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data=button_id)]
        for button_id, text in buttons_data.items()
    ])
    return inline_kb


def return_button():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='return')],
    ])
    return inline_kb
