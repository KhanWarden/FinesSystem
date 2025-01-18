from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

router = Router()


@router.callback_query(F.data == "penalties_admin")
async def penalties_handler(call: CallbackQuery):
    pass
