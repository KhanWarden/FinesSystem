from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from app.keyboards.inline_kbs import certificates_kb, main_kb

router = Router()


@router.callback_query(F.data == "certificates")
async def certificate_start_handler(call: CallbackQuery):
    await call.message.edit_text("Что хотите сделать?", reply_markup=certificates_kb())


@router.callback_query(F.data == "to_main_menu")
async def to_main_menu_handler(call: CallbackQuery):
    await call.message.edit_text(
        text="На стадии разработки...",
        reply_markup=main_kb()
    )


@router.callback_query(F.data == "create_new_cert")
async def create_new_cert_handler(call: CallbackQuery):
    await call.message.answer("Вот ваш новый сертификат:")
    