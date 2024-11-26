from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.database import delete_admin_from_users, get_employees, add_employee, get_total_employees, delete_employee, \
    get_admins, get_total_admins, get_total_non_admins, get_non_admins, rename_employee, change_position_func
from app.keyboards.inline_kbs import (main_kb, admin_panel_kb, interrupt_employee_admin_panel,
                                      back_to_employees_admin_panel_kb, EmployeeCallback,
                                      create_employees_pagination_kb,
                                      create_non_admins_pagination_kb, NonAdminCallback,
                                      create_admins_pagination_kb, AdminCallback, EmployeeDeleteCallback,
                                      employees_to_delete_pagination_kb)
from app.states import AdminStates
from app.database import make_admin

router = Router()


@router.callback_query(F.data == "to_main_menu")
async def to_main_menu(call: CallbackQuery):
    await call.message.edit_text(
        text=f"Добро пожаловать, {call.from_user.first_name}!",
        reply_markup=(await main_kb(call.from_user.id))
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
    await state.update_data(name=name)
    await message.answer("Теперь введите должность сотрудника")
    await state.set_state(AdminStates.wait_for_position_new_employee)


@router.message(AdminStates.wait_for_position_new_employee)
async def wait_for_position_new_employee(message: Message, state: FSMContext):
    position = message.text

    data = await state.get_data()
    user_id = data.get("user_id")
    name = data.get("name")

    if await add_employee(user_id, name, position):
        await message.answer(f"{name} добавлен в список сотрудников.")
        await message.answer(text=f"Добро пожаловать, {message.from_user.full_name}!",
                             reply_markup=interrupt_employee_admin_panel())
        await state.clear()
    else:
        await message.answer(f"Сотрудник с таким именем уже существует!",
                             reply_markup=interrupt_employee_admin_panel())
        await state.clear()


@router.callback_query(F.data == "delete_employee")
async def delete_employee_handler(call: CallbackQuery):
    total_employees = await get_total_employees()
    employees = await get_employees(0)
    keyboard = employees_to_delete_pagination_kb(employees, 0, total_employees, action="delete_employee")
    await call.message.edit_text("Выберите сотрудника для удаления",
                                 reply_markup=keyboard)


@router.callback_query(F.data.startswith("page_"))
async def paginate_employees(call: CallbackQuery):
    page = int(call.data.split("_")[1])
    total_employees = await get_total_employees()

    employees = await get_employees(page)
    keyboard = employees_to_delete_pagination_kb(employees, page, total_employees, action="delete_employee")
    await call.message.edit_text("Выберите сотрудника для удаления",
                                 reply_markup=keyboard)

    await call.answer()


@router.callback_query(EmployeeDeleteCallback.filter(F.action == "delete_employee"))
async def handle_delete_employee(call: CallbackQuery, callback_data: EmployeeDeleteCallback):
    name = callback_data.name
    await delete_employee(name)
    await call.message.edit_text(f"Сотрудник {name} удалён.",
                                 reply_markup=interrupt_employee_admin_panel())


@router.callback_query(F.data == "add_admin")
async def add_admin_handler(call: CallbackQuery):
    non_admins = await get_non_admins(0)
    total_non_admins = await get_total_non_admins()

    keyboard = create_non_admins_pagination_kb(non_admins, 0, total_non_admins, action="make_admin")

    await call.message.edit_text("Выберите сотрудника, которому хотите дать права администратора",
                                 reply_markup=keyboard)


@router.callback_query(F.data.startswith("non_admin_page_"))
async def paginate_non_admins(call: CallbackQuery):
    page = int(call.data.split("_")[3])
    total_non_admins = await get_total_non_admins()

    admins = await get_non_admins(page)
    keyboard = create_non_admins_pagination_kb(admins, page, total_non_admins, action="make_admin")
    await call.message.edit_text("Выберите сотрудника, которому хотите дать права администратора",
                                 reply_markup=keyboard)

    await call.answer()


@router.callback_query(NonAdminCallback.filter(F.action == "make_admin"))
async def make_admin_handler(call: CallbackQuery, callback_data: NonAdminCallback):
    name = callback_data.name
    await make_admin(name)
    await call.message.edit_text(text=f"{name} добавлен в список администраторов.",
                                 reply_markup=interrupt_employee_admin_panel())


@router.callback_query(F.data == "remove_admin")
async def delete_admin_handler(call: CallbackQuery):
    admins = await get_admins(0)
    total_admins = await get_total_admins()
    keyboard = create_admins_pagination_kb(admins, 0, total_admins, action="delete_admin")

    await call.message.edit_text("Выберите сотрудника, у которого хотите отнять права администратора",
                                 reply_markup=keyboard)


@router.callback_query(F.data.startswith("admin_page_"))
async def paginate_admins(call: CallbackQuery):
    page = int(call.data.split("_")[2])
    total_admins = await get_total_admins()

    admins = await get_admins(page)
    keyboard = create_non_admins_pagination_kb(admins, page, total_admins, action="delete_admin")
    await call.message.edit_text("Выберите сотрудника, которому хотите дать права администратора",
                                 reply_markup=keyboard)

    await call.answer()


@router.callback_query(AdminCallback.filter(F.action == "delete_admin"))
async def delete_admin_handler_(call: CallbackQuery, callback_data: AdminCallback):
    name = callback_data.name
    await delete_admin_from_users(name)
    await call.message.edit_text(text=f"Сотрудник {name} удалён из списка администраторов.",
                                 reply_markup=interrupt_employee_admin_panel())


@router.callback_query(F.data == "rename_employee")
async def rename_employee_handler(call: CallbackQuery):
    total_employees = await get_total_employees()
    employees = await get_employees(0)
    keyboard = create_employees_pagination_kb(employees, 0, total_employees, action="rename_employee")
    await call.message.edit_text("Выберите сотрудника, которому хотите изменить имя",
                                 reply_markup=keyboard)


@router.callback_query(F.data.startswith("page_"))
async def paginate_employees(call: CallbackQuery):
    page = int(call.data.split("_")[1])
    total_employees = await get_total_employees()

    employees = await get_employees(page)
    keyboard = create_employees_pagination_kb(employees, page, total_employees, action="rename_employee")
    await call.message.edit_text("Выберите сотрудника, которому хотите изменить имя",
                                 reply_markup=keyboard)

    await call.answer()


@router.callback_query(EmployeeCallback.filter(F.action == "rename_employee"))
async def rename_employee_handler_(call: CallbackQuery, callback_data: EmployeeCallback, state: FSMContext):
    name = callback_data.name
    await state.update_data(name=name)
    await call.message.edit_text(f"Введите имя на которое хотите изменить")
    await state.set_state(AdminStates.change_name)


@router.message(AdminStates.change_name)
async def change_name_state(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]
    new_name = message.text
    if await rename_employee(name, new_name):
        await message.answer("Имя сотрудника изменено.",
                             reply_markup=interrupt_employee_admin_panel())
        await state.clear()
    else:
        await message.answer(f"{new_name} уже есть в списке.")


@router.callback_query(F.data == "change_position")
async def change_position_handler(call: CallbackQuery):
    total_employees = await get_total_employees()
    employees = await get_employees(0)
    keyboard = create_employees_pagination_kb(employees, 0, total_employees, action="change_position")
    await call.message.edit_text("Выберите сотрудника, которому хотите изменить должность",
                                 reply_markup=keyboard)


@router.callback_query(F.data.startswith("page_"))
async def paginate_employees(call: CallbackQuery):
    page = int(call.data.split("_")[1])
    total_employees = await get_total_employees()

    employees = await get_employees(page)
    keyboard = create_employees_pagination_kb(employees, page, total_employees, action="change_position")
    await call.message.edit_text("Выберите сотрудника, которому хотите изменить должность",
                                 reply_markup=keyboard)

    await call.answer()


@router.callback_query(EmployeeCallback.filter(F.action == "change_position"))
async def change_position_handler_(call: CallbackQuery, callback_data: EmployeeCallback, state: FSMContext):
    name = callback_data.name
    await state.update_data(name=name)

    await call.message.edit_text(f"Введите название должности")
    await state.set_state(AdminStates.change_position)


@router.message(AdminStates.change_position)
async def change_position_state(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]
    new_position = message.text

    await change_position_func(name, new_position)
    await message.answer(f"Должность <b>{name}</b> была изменена на <b>{new_position}</b>",
                         reply_markup=interrupt_employee_admin_panel())
    await state.clear()
