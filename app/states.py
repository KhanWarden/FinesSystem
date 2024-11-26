from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    wait_for_user_id = State()
    wait_for_admin_id = State()
    wait_for_new_employee_id = State()
    wait_for_new_employee_name = State()
    wait_for_position_new_employee = State()
    change_name = State()
    change_position = State()


class CalculatorStates(StatesGroup):
    waiting_for_guests_amount = State()
    waiting_for_duration = State()
    waiting_for_range_value = State()
    waiting_for_percentage_discount = State()
    waiting_for_numerical_discount = State()


class CertificateStates(StatesGroup):
    date_from_user = State()
    id_of_certificate = State()


class BarrierStates(StatesGroup):
    add_user = State()