from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.keyboards.inline_kbs import main_kb

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    if message.chat.type == 'private':
        user_id = message.from_user.id
        await message.answer(f"Добро пожаловать, {message.from_user.first_name}!",
                             reply_markup=await main_kb(telegram_id=user_id))
    else:
        await message.delete()
        await message.answer("Бот работает только в ЛС.")
