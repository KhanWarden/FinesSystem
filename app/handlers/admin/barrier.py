from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from app.database import add_user_to_barrier, delete_employee, get_all_users_from_barrier, delete_user_from_barrier, \
    add_user_to_gate, get_all_users_from_gate, delete_user_from_gate
from app.keyboards.inline_kbs import admin_barrier_kb, users_to_delete_from_barrier_pagination_kb, UsersBarrier, \
    admin_gate_kb, users_to_delete_from_gate_pagination_kb
from app.states import BarrierStates

router = Router()


@router.callback_query(F.data == "barrier_admin")
async def barrier_admin_handler(call: CallbackQuery):
    await call.message.edit_text("Выберите что нужно сделать",
                                 reply_markup=admin_barrier_kb())


@router.callback_query(F.data == "add_user_to_barrier")
async def add_user_to_barrier_handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите тэг пользователя")
    await state.set_state(BarrierStates.username_barrier)


@router.message(BarrierStates.username_barrier)
async def add_user_to_barrier_handler_(message: Message, state: FSMContext):
    username = message.text
    if username.startswith("@"):
        await add_user_to_barrier(username)
        await message.answer(f"{username} добавлен в список сотрудников с доступом к шлагбауму",
                             reply_markup=admin_barrier_kb())
    else:
        await message.answer("Тэг должен начинаться с @")

    await state.clear()


@router.callback_query(F.data == "delete_user_from_barrier")
async def delete_user_from_barrier_handler(call: CallbackQuery):
    users = await get_all_users_from_barrier()
    await call.message.edit_text("Выберите сотрудника, у которого больше нет доступа",
                                 reply_markup=users_to_delete_from_barrier_pagination_kb(users))


@router.callback_query(UsersBarrier.filter(F.action == "delete_user_from_barrier"))
async def delete_user_from_barrier_handler_(call: CallbackQuery, callback_data: UsersBarrier):
    username = callback_data.username
    await delete_user_from_barrier(username)
    await call.message.edit_text(f"{username} удалён из списка.",
                                 reply_markup=admin_barrier_kb())


@router.callback_query(F.data == "gate_admin")
async def gate_admin_handler(call: CallbackQuery):
    await call.message.edit_text("Выберите что нужно сделать",
                                 reply_markup=admin_gate_kb())


@router.callback_query(F.data == "add_user_to_gate")
async def add_user_to_gate_handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите тэг пользователя")
    await state.set_state(BarrierStates.username_gate)


@router.message(BarrierStates.username_gate)
async def add_user_to_gate_handler_(message: Message, state: FSMContext):
    username = message.text
    if username.startswith("@"):
        await add_user_to_gate(username)
        await message.answer(f"{username} добавлен в список сотрудников с доступом к воротам",
                             reply_markup=admin_gate_kb())
    else:
        await message.answer("Тэг должен начинаться с @")

    await state.clear()


@router.callback_query(F.data == "delete_user_from_gate")
async def delete_user_from_gate_handler(call: CallbackQuery):
    users = await get_all_users_from_gate()
    await call.message.edit_text("Выберите сотрудника, у которого больше нет доступа",
                                 reply_markup=users_to_delete_from_gate_pagination_kb(users))


@router.callback_query(UsersBarrier.filter(F.action == "delete_user_from_gate"))
async def delete_user_from_barrier_handler_(call: CallbackQuery, callback_data: UsersBarrier):
    username = callback_data.username
    await delete_user_from_gate(username)
    await call.message.edit_text(f"{username} удалён из списка.",
                                 reply_markup=admin_gate_kb())
