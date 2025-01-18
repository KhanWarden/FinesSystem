from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from app.database import get_unmuted_users_from_barrier, get_all_users_from_barrier, add_user_to_barrier, mute_user, \
    unmute_user, get_all_users_from_gate
from app.keyboards.inline_kbs import open_kb, main_kb, gate_kb

router = Router()


@router.message(Command('open'))
async def open_barrier_handler(message: Message):
    username = message.from_user.username

    await message.delete()
    users = await get_unmuted_users_from_barrier()
    await message.answer(f"Запрос на открытие шлагбаума от @{username}.\n\n{" ".join(users)}",
                         reply_markup=open_kb("Не открыто"))


@router.callback_query(F.data == "open_barrier")
async def button_handler(call: CallbackQuery):
    user = f"@{call.from_user.username}"
    import re
    text = call.message.text
    result = re.sub(r'\..*', '', text, flags=re.DOTALL)

    if user in await get_all_users_from_barrier():
        await call.message.edit_text(text=result,
                                     reply_markup=open_kb(f"✅ {user} открыл ✅"))
    else:
        await call.answer("У вас нет доступа!", show_alert=True)


@router.message(Command("gate"))
async def gate_barrier_handler(message: Message):
    username = message.from_user.username

    await message.delete()
    users = await get_all_users_from_gate()
    await message.answer(f"Запрос на открытие ворот с Айтиева от @{username}.\n\n{" ".join(users)}",
                         reply_markup=gate_kb("Не открыто"))


@router.callback_query(F.data == "gate_barrier")
async def button_handler(call: CallbackQuery):
    user = f"@{call.from_user.username}"
    import re
    text = call.message.text
    result = re.sub(r'\..*', '', text, flags=re.DOTALL)

    if user in await get_all_users_from_gate():
        await call.message.edit_text(text=result,
                                     reply_markup=open_kb(f"✅ {user} открыл ✅"))
    else:
        await call.answer("У вас нет доступа!", show_alert=True)


@router.message(Command("mute"))
async def mute_notifications_handler(message: Message):
    user = f"@{message.from_user.username}"
    user_id = message.from_user.id

    await mute_user(user)

    await message.answer("Бот больше не будет вас тэгать.",
                         reply_markup=await main_kb(user_id))


@router.message(Command("unmute"))
async def unmute_notifications_handler(message: Message):
    user = f"@{message.from_user.username}"
    user_id = message.from_user.id

    await unmute_user(user)

    await message.answer("Бот снова будет вас тэгать.",
                         reply_markup=await main_kb(user_id))
