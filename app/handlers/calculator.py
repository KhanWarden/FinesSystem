from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.keyboards.inline_kbs import game_counter, return_button
from app.states import CalculatorStates

router = Router()

buttons = {
    "button_guests_amount": "Количество участников",
    "button_game_duration": "Длительность игры",
    "button_discount": "Скидка"
}


@router.message(CommandStart())
async def start_function(message: Message):
    await message.answer("privet")


@router.message(Command('count'))
async def count_sum(message: Message, state: FSMContext):
    await state.update_data(buttons=buttons.copy())
    await message.answer('Ниже кнопки. Нажмите на необходимую для изменения информации.',
                         reply_markup=game_counter(buttons))


@router.callback_query(F.data == "return")
async def return_button_handler(call: CallbackQuery):
    await call.message.edit_text(
        text="Ниже кнопки. Нажмите на необходимую для изменения информации.",
        reply_markup=game_counter(buttons)
    )


@router.callback_query(F.data == "button_guests_amount")
async def button_guests_amount_handler(call: CallbackQuery, state: FSMContext):
    await state.update_data(button_1="button_guests_amount")
    await call.message.edit_text(
        text="Введите количество гостей",
        reply_markup=return_button()
    )
    await state.set_state(CalculatorStates.waiting_for_guests_amount)
    await call.answer()


@router.message(CalculatorStates.waiting_for_guests_amount)
async def process_input(message: Message, state: FSMContext):
    guests_amount = message.text

    data = await state.get_data()
    _buttons = data.get("buttons")
    button_id = data.get("button_1")
    _buttons[button_id] = f"Количество участников: {guests_amount}"
    await state.update_data(buttons=_buttons)

    await message.answer(
        text="Ниже кнопки. Нажмите на необходимую для изменения информации.",
        reply_markup=game_counter(_buttons)
    )
    await state.clear()


@router.callback_query(F.data == "button_game_duration")
async def button_game_duration_handler(call: CallbackQuery, state: FSMContext):
    await state.update_data(button_2="button_game_duration")
    await call.message.edit_text(
        text="Введите длительность в минутах (60 / 90 / 120)",
        reply_markup=return_button()
    )
    await state.set_state(CalculatorStates.waiting_for_duration)
    await call.answer()


@router.message(CalculatorStates.waiting_for_duration)
async def process_input(message: Message, state: FSMContext):
    duration = message.text

    data = await state.get_data()
    _buttons = data.get("buttons")
    button_id = data.get("button_2")
    _buttons[button_id] = f"Длительность игры: {duration} мин."
    await state.update_data(buttons=_buttons)

    await message.answer(
        text="Ниже кнопки. Нажмите на необходимую для изменения информации.",
        reply_markup=game_counter(_buttons)
    )
    await state.clear()


@router.callback_query(F.data == "button_discount")
async def button_game_duration_handler(call: CallbackQuery, state: FSMContext):
    await state.update_data(button_3="button_discount")
    await call.message.edit_text(
        text="Введите скидку в процентах (просто числом без знака)",
        reply_markup=return_button()
    )
    await state.set_state(CalculatorStates.waiting_for_discount)
    await call.answer()


@router.message(CalculatorStates.waiting_for_discount)
async def process_input(message: Message, state: FSMContext):
    discount = message.text

    data = await state.get_data()
    _buttons = data.get("buttons")
    button_id = data.get("button_3")
    _buttons[button_id] = f"Скидка: {discount}%"
    await state.update_data(buttons=_buttons)

    await message.answer(
        text="Ниже кнопки. Нажмите на необходимую для изменения информации.",
        reply_markup=game_counter(_buttons)
    )
    await state.clear()
