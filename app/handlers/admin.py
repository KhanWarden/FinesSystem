from pathlib import Path

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.database.admins import is_admin
from app.keyboards.inline_kbs import main_kb
from app.states import AdminStates
from app.keyboards.reply_kbs import main_menu
from app.database import make_admin

router = Router()


@router.message(Command('add_admin'))
async def add_admin(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("У вас недостаточно прав для выполнения этой команды.")
        await message.answer("На стадии разработки...", reply_markup=(main_kb(message.from_user.id)))
        return

    await message.answer("Введите ID пользователя: ")
    await state.set_state(AdminStates.wait_for_admin_id)


@router.message(AdminStates.wait_for_admin_id)
async def wait_for_add_admin(message: Message, state: FSMContext):
    user_id = int(message.text)
    await make_admin(user_id)
    await message.answer(f"ID {user_id} добавлен в список администраторов.")
    await state.clear()
