from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class UsersBarrier(CallbackData, prefix="user"):
    action: str
    username: str


def admin_barrier_kb():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Добавить сотрудника", callback_data="add_user_to_barrier")],
        [InlineKeyboardButton(text="🔴 Удалить сотрудника", callback_data="delete_user_from_barrier"),],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data='admin_panel')]
    ])
    return inline_kb


def admin_gate_kb():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Добавить сотрудника", callback_data="add_user_to_gate")],
        [InlineKeyboardButton(text="🔴 Удалить сотрудника", callback_data="delete_user_from_gate")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data='admin_panel')]
    ])
    return inline_kb


def users_to_delete_from_barrier_pagination_kb(users: list):
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[])

    for username in users:
        inline_kb.inline_keyboard.append(
            [InlineKeyboardButton(
                text=username,
                callback_data=UsersBarrier(action="delete_user_from_barrier", username=username).pack()
            )]
        )

    back_button = [InlineKeyboardButton(text="⬅️ Назад", callback_data="barrier_admin")]
    inline_kb.inline_keyboard.append(back_button)
    return inline_kb


def users_to_delete_from_gate_pagination_kb(users: list):
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[])

    for username in users:
        inline_kb.inline_keyboard.append(
            [InlineKeyboardButton(
                text=username,
                callback_data=UsersBarrier(action="delete_user_from_gate", username=username).pack()
            )]
        )

    back_button = [InlineKeyboardButton(text="⬅️ Назад", callback_data="gate_admin")]
    inline_kb.inline_keyboard.append(back_button)
    return inline_kb
