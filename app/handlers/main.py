from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.keyboards.inline_kbs import main_kb

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    await message.answer("На стадии разработки...",
                         reply_markup=await main_kb(telegram_id=user_id))
