from pathlib import Path

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.states import AdminStates
from app.keyboards.reply_kbs import main_menu
from app.database.admins import AdminDatabase

project_folder = Path(__file__).parent.parent.parent
database_path = project_folder / 'database.db'

admin_database = AdminDatabase(database_path)
router = Router()


@router.message(CommandStart())
async def command_start(message: Message):
    await message.answer(main_menu(message.from_user.id, database_path))


@router.message(Command('add_admin'))
async def add_admin(message: Message, state: FSMContext):
    await message.answer("Введите ID телеграма пользователя: ")
    await state.set_state(AdminStates.wait_for_admin_id)
    admin_database.add_admin_from_users(message.from_user.id)


@router.message(AdminStates.wait_for_admin_id)
async def wait_for_admin(message: Message, state: FSMContext):
    await state.update_data(admin_id=message.text)
    await message.answer("ID добавлен.", main_menu(message.from_user.id, database_path))
    await state.clear()
