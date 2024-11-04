from aiogram import Router, F, Dispatcher
from aiogram.types import Message, CallbackQuery

router = Router()


@router.callback_query(F.data == "my_profile")
async def my_profile_handler(call: CallbackQuery):
    await call.answer(text="В разработке", show_alert=True)