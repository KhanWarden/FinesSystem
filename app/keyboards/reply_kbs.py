from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def durations():
    kb_list = [
        [KeyboardButton(text='60'), KeyboardButton(text='90'), KeyboardButton(text='120')]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
