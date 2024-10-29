from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    wait_for_admin_id = State()


class CalculatorStates(StatesGroup):
    waiting_for_guests_amount = State()
    waiting_for_duration = State()
    waiting_for_range_value = State()
    waiting_for_percentage_discount = State()
    waiting_for_numerical_discount = State()
