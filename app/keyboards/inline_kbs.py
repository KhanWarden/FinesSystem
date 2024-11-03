from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database import is_admin


class EmployeeCallback(CallbackData, prefix="employee"):
    action: str
    name: str


class NonAdminCallback(CallbackData, prefix="non_admin"):
    action: str
    name: str


class AdminCallback(CallbackData, prefix="admin"):
    action: str
    name: str


async def main_kb(telegram_id):
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Калькулятор", callback_data='count'),
         InlineKeyboardButton(text="❗️ Штрафы", callback_data='penalties')],

        [InlineKeyboardButton(text="📄 Сертификаты", callback_data='certificates')],
        [InlineKeyboardButton(text="👤 Мой Профиль", callback_data="my_profile")]
    ])
    if await is_admin(telegram_id):
        inline_kb.inline_keyboard.append([InlineKeyboardButton(text="⚙️ Админ панель", callback_data="admin_panel")])
    return inline_kb


def admin_panel_kb():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Сотрудники", callback_data='employees')],
        [InlineKeyboardButton(text="❗️ Штрафы", callback_data='penalties_admin')],
        [InlineKeyboardButton(text="↩️ В главное меню", callback_data='to_main_menu')]
    ])
    return inline_kb


def interrupt_employee_admin_panel():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Добавить", callback_data='add_employee'),
         InlineKeyboardButton(text="🔴 Удалить", callback_data='delete_employee')],
        [InlineKeyboardButton(text="📌 Дать права администратора", callback_data='add_admin')],
        [InlineKeyboardButton(text="⚠️ Забрать права администратора", callback_data='remove_admin')],
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


def create_employees_pagination_kb(employees, page, total_employees, action):
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


def create_non_admins_pagination_kb(non_admins, page, total_non_admins, action):
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[])

    for non_admin in non_admins:
        inline_kb.inline_keyboard.append(
            [InlineKeyboardButton(
                text=non_admin,
                callback_data=NonAdminCallback(action=action, name=non_admin).pack()
            )]
        )

    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"non_admin_page_{page - 1}"))

    pagination_buttons.append(InlineKeyboardButton(text="↩️ В меню", callback_data="employees"))

    if (page + 1) * 5 < total_non_admins:
        pagination_buttons.append(InlineKeyboardButton(text="➡️ Вперед", callback_data=f"non_admin_page_{page + 1}"))

    inline_kb.inline_keyboard.append(pagination_buttons)
    return inline_kb


def create_admins_pagination_kb(admins, page, total_admins, action):
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[])

    for admin in admins:
        inline_kb.inline_keyboard.append(
            [InlineKeyboardButton(
                text=admin,
                callback_data=AdminCallback(action=action, name=admin).pack()
            )]
        )

    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"admins_page_{page - 1}"))

    pagination_buttons.append(InlineKeyboardButton(text="↩️ В меню", callback_data="employees"))

    if (page + 1) * 5 < total_admins:
        pagination_buttons.append(InlineKeyboardButton(text="➡️ Вперед", callback_data=f"admins_page_{page + 1}"))

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
