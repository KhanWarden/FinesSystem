from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def open_kb(status: str):
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=status, callback_data='open_barrier')],
    ])
    return inline_kb


def gate_kb(status: str):
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=status, callback_data='gate_barrier')],
    ])
    return inline_kb
