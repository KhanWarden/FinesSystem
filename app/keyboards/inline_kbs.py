from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database import is_admin


class EmployeeCallback(CallbackData, prefix="employee"):
    action: str
    name: str


async def main_kb(telegram_id):
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Калькулятор", callback_data='count'),
         InlineKeyboardButton(text="❗️ Штрафы", callback_data='penalties')],

        [InlineKeyboardButton(text="📄 Печать Сертификатов", callback_data='certificates')],
        [InlineKeyboardButton(text="👤 Мой Профиль", callback_data="my_profile")]
    ])
    if await is_admin(telegram_id):
        inline_kb.inline_keyboard.append([InlineKeyboardButton(text="⚙️ Админ панель", callback_data="admin_panel")])
    return inline_kb


def admin_panel_kb():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Сотрудники", callback_data='employees')],
        [InlineKeyboardButton(text="📄 Сертификаты", callback_data='certificate_admin')],
        [InlineKeyboardButton(text="❗️ Штрафы", callback_data='penalties_admin')],
        [InlineKeyboardButton(text="↩️ В главное меню", callback_data='to_main_menu')]
    ])
    return inline_kb


def interrupt_employee_admin_panel():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Добавить", callback_data='add_employee'),
         InlineKeyboardButton(text="🔴 Удалить", callback_data='delete_employee')],
        [InlineKeyboardButton(text="📌 Дать права администратора", callback_data='add_admin')],
        [InlineKeyboardButton(text="⚠️ Забрать права администратора", callback_data='delete_admin')],
        [InlineKeyboardButton(text="🖊 Изменить имя сотрудника", callback_data='rename_employee')],
        [InlineKeyboardButton(text="🖊 Изменить должность сотрудника", callback_data='change_position')],
        [InlineKeyboardButton(text="↩️ Назад", callback_data='admin_panel')]
    ])
    return inline_kb


def back_to_admin_panel_kb():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data='back_to_admin_panel'), ]
    ])
    return inline_kb


def back_to_employees_admin_panel_kb():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="employees"), ]
    ])
    return inline_kb


def create_pagination_kb(employees, page, total_employees, action):
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[])

    for employee in employees:
        inline_kb.inline_keyboard.append(
            [InlineKeyboardButton(
                text=employee,
                callback_data=EmployeeCallback(action=action, name=employee).pack()
            )]
        )

    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{page - 1}"))

    pagination_buttons.append(InlineKeyboardButton(text="↩️ В меню", callback_data="employees"))

    if (page + 1) * 5 < total_employees:
        pagination_buttons.append(InlineKeyboardButton(text="➡️ Вперед", callback_data=f"page_{page + 1}"))

    inline_kb.inline_keyboard.append(pagination_buttons)
    return inline_kb


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


def certificates_kb():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Создать новый", callback_data="create_new_cert"),
         InlineKeyboardButton(text="🔍 Проверить сертификат", callback_data="check_cert")],
        [InlineKeyboardButton(text="↩️ Вернуться в главное меню", callback_data="to_main_menu")]
    ])
    return inline_kb
