from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.database import delete_admin_from_users, get_employees, add_employee, get_total_employees, delete_employee, \
    get_admins, get_total_admins
from app.keyboards.inline_kbs import main_kb, admin_panel_kb, back_to_admin_panel_kb, \
    interrupt_employee_admin_panel, back_to_employees_admin_panel_kb, EmployeeCallback, create_pagination_kb
from app.states import AdminStates
from app.database import make_admin

router = Router()


@router.callback_query(F.data == "to_main_menu")
async def to_main_menu(call: CallbackQuery):
    await call.message.edit_text(
        text="На стадии разработки...",
        reply_markup=(await main_kb(call.from_user.id))
    )


@router.callback_query(F.data == "admin_panel")
async def admin_panel(call: CallbackQuery):
    await call.message.edit_text(
        text=f"Добро пожаловать, {call.from_user.full_name}!",
        reply_markup=admin_panel_kb()
    )


@router.callback_query(F.data == "employees")
async def employees_handler(call: CallbackQuery):
    await call.message.edit_text("Выберите нужную кнопку для взаимодействия с сотрудниками",
                                 reply_markup=interrupt_employee_admin_panel())


@router.callback_query(F.data == "back_to_admin_panel")
async def back_to_admin_panel_handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=f"Добро пожаловать, {call.from_user.full_name}!",
                                 reply_markup=admin_panel_kb())
    await state.clear()


@router.callback_query(F.data == "add_admin")
async def add_admin_handler(call: CallbackQuery):
    page = int(call.data.split("_")[1])
    employees = await get_employees(page)
    total_employees = get_total_employees()

    keyboard = create_pagination_kb(employees, page, total_employees, action="make_admin")

    await call.message.edit_text("Выберите сотрудника, которому хотите дать права администратора",
                                 reply_markup=keyboard())


@router.callback_query(EmployeeCallback.filter(F.action == "make_admin"))
async def make_admin_handler(call: CallbackQuery, callback_data: EmployeeCallback):
    name = callback_data.name
    await make_admin(name)
    await call.message.edit_text(text=f"{name} добавлен в список администраторов.",
                                 reply_markup=interrupt_employee_admin_panel())


@router.callback_query(F.data == "delete_admin")
async def delete_admin_handler(call: CallbackQuery):
    page = int(call.data.split("_")[1])
    admins = await get_admins(page)
    total_admins = get_total_admins()
    keyboard = create_pagination_kb(admins, page, total_admins, action="delete_admin")

    await call.message.edit_text("Выберите сотрудника, у которого хотите отнять права администратора",
                                 reply_markup=keyboard())


@router.callback_query(EmployeeCallback.filter(F.action == "delete_admin"))
async def delete_admin_handler_(call: CallbackQuery, callback_data: EmployeeCallback):
    name = callback_data.name
    await delete_admin_from_users(name)
    await call.message.edit_text(text=f"Сотрудник {name} удалён из списка администраторов.",
                                 reply_markup=interrupt_employee_admin_panel())


@router.callback_query(F.data == "add_employee")
async def add_employee_handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Введите ID пользователя",
                                 reply_markup=back_to_employees_admin_panel_kb())
    await state.set_state(AdminStates.wait_for_new_employee_id)


@router.message(AdminStates.wait_for_new_employee_id)
async def wait_for_new_employee_to_add(message: Message, state: FSMContext):
    user_id = int(message.text)
    await state.update_data(user_id=user_id)
    await message.answer("Теперь введите имя нового сотрудника")
    await state.set_state(AdminStates.wait_for_new_employee_name)


@router.message(AdminStates.wait_for_new_employee_name)
async def wait_for_new_employee_name(message: Message, state: FSMContext):
    name = message.text

    data = await state.get_data()
    user_id = data.get("user_id")
    await add_employee(user_id, name)
    await message.answer(f"{name} добавлен в список сотрудников.")
    await message.answer(text=f"Добро пожаловать, {message.from_user.full_name}!",
                         reply_markup=admin_panel_kb())
    await state.clear()


@router.callback_query(F.data == "delete_employee")
async def delete_employee_handler(call: CallbackQuery):
    total_employees = await get_total_employees()
    employees = await get_employees(0)
    keyboard = create_pagination_kb(employees, 0, total_employees, action="delete")
    await call.message.edit_text("Выберите сотрудника для удаления",
                                 reply_markup=keyboard)


# TODO: PAGINATION
@router.callback_query(F.data.startswith("page_"))
async def paginate_employees(call: CallbackQuery):
    page = int(call.data.split("_")[1])
    action = call.data.split("_")[0]

    if action == "delete":
        employees = await get_employees(page)
        keyboard = create_pagination_kb(employees, page, total_employees=await get_total_employees(), action="delete")
        await call.message.edit_text("Выберите сотрудника для удаления",
                                     reply_markup=keyboard)
    if action == "make_admin":
        total_employees = await get_total_employees()

    await call.answer()


@router.callback_query(EmployeeCallback.filter(F.action == "delete"))
async def handle_delete_employee(call: CallbackQuery, callback_data: EmployeeCallback):
    name = callback_data.name
    await delete_employee(name)
    await call.message.edit_text(f"Сотрудник {name} удалён.",
                                 reply_markup=interrupt_employee_admin_panel())
