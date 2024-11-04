from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .admin_employees import (AdminCallback, NonAdminCallback, EmployeeCallback, EmployeeDeleteCallback,
                              admin_panel_kb, back_to_admin_panel_kb,
                              interrupt_employee_admin_panel, back_to_employees_admin_panel_kb,
                              employees_to_delete_pagination_kb, create_non_admins_pagination_kb,
                              create_admins_pagination_kb, create_employees_pagination_kb)
from .certificate_kbs import (certificates_kb, certificates_sum_kb,
                              certificate_date_for_5k_kb, certificate_date_for_10k_kb)
from .calculator_kbs import game_counter, prepayment_button, return_button


__all__ = ['main_kb',

           'AdminCallback', 'NonAdminCallback', 'EmployeeCallback', 'EmployeeDeleteCallback',
           'admin_panel_kb',
           'back_to_admin_panel_kb',
           'interrupt_employee_admin_panel',
           'back_to_employees_admin_panel_kb',
           'employees_to_delete_pagination_kb',
           'create_non_admins_pagination_kb',
           'create_admins_pagination_kb',
           'create_employees_pagination_kb',

           'certificates_kb',
           'certificates_sum_kb',
           'certificate_date_for_5k_kb',
           'certificate_date_for_10k_kb',

           'game_counter',
           'prepayment_button',
           'return_button']

from ...database import is_admin


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
