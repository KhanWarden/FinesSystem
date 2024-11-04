from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

router = Router()


@router.callback_query(F.data == "penalties")
async def penalties_start_handler(call: CallbackQuery):
    await call.answer("В разработке", show_alert=True)
