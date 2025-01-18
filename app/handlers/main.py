from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.keyboards.inline_kbs import main_kb
from app.methods import is_only_digits

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


@router.message(Command("link"))
async def id_handler(message: Message):
    arg = message.text.split(" ")
    if is_only_digits(arg[1]):
        await message.delete()
        link = f"https://plus-erp.app/sales/order/preview/{arg}?tab=description"
        await message.answer(link)
    else:
        return
