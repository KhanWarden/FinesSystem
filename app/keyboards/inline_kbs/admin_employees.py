from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class EmployeeCallback(CallbackData, prefix="employee"):
    action: str
    name: str


class EmployeeDeleteCallback(CallbackData, prefix="todelete"):
    action: str
    name: str


class NonAdminCallback(CallbackData, prefix="non_admin"):
    action: str
    name: str


class AdminCallback(CallbackData, prefix="admin"):
    action: str
    name: str


def admin_panel_kb():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Сотрудники", callback_data='employees')],
        [InlineKeyboardButton(text="❗️ Штрафы", callback_data='penalties_admin')],
        [InlineKeyboardButton(text="↩️ В главное меню", callback_data='to_main_menu')]
    ])
    return inline_kb


def back_to_admin_panel_kb():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data='back_to_admin_panel'), ]
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


def back_to_employees_admin_panel_kb():
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="employees"), ]
    ])
    return inline_kb


def employees_to_delete_pagination_kb(employees, page, total_employees, action):
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[])

    for employee in employees:
        inline_kb.inline_keyboard.append(
            [InlineKeyboardButton(
                text=employee,
                callback_data=EmployeeDeleteCallback(action=action, name=employee).pack()
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
