from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.keyboards.inline_kbs import main_kb

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    inline_kb = main_kb()
    # if message.from_user.id in admins:
    #     inline_kb.append(InlineKeyboardButton(text="⚙️ Админ панель", callback_data="admin_panel"))
    await message.answer("На стадии разработки...",
                         reply_markup=main_kb())
