from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.keyboards.inline_kbs import game_counter, return_button, prepayment_button
from app.keyboards.reply_kbs import durations
from app.methods.parser import parse_value
from app.states import CalculatorStates
from app.methods.calculator_methods import detailed_count_game_sum, count_game_sum

router = Router()

buttons = {
    "button_guests_amount": "👥 Количество участников",
    "button_game_duration": "🕒 Длительность игры",
    "button_range": "📍 Доплата за дальность",
    "button_percentage_discount": "📉 Скидка в процентах",
    "button_numerical_discount": "💸 Скидка в сумме",
    "button_do_nothing": " ",
    "button_prepayment": "💳 Предоплата",
    "button_done": "======== Рассчитать ========"
}


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Пока доступна только команда /count\n\nВ стадии разработки...")


@router.message(Command('count'))
async def count_sum(message: Message, state: FSMContext):
    await state.update_data(buttons=buttons.copy())
    await message.answer('Ниже кнопки. Нажмите на необходимую для изменения информации.',
                         reply_markup=game_counter(buttons))


@router.callback_query(F.data == "return")
async def return_button_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    _buttons = data.get("buttons")

    await call.message.edit_text(
        text="Ниже кнопки. Нажмите на необходимую для изменения информации.",
        reply_markup=game_counter(_buttons)
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
    if int(message.text) < 0:
        await message.answer("Неверные данные!")
        return
    else:
        guests_amount = message.text

    data = await state.get_data()
    _buttons = data.get("buttons")
    button_id = data.get("button_1")
    _buttons[button_id] = f"👥 Количество участников: {guests_amount}"
    await state.update_data(buttons=_buttons)

    await message.answer(
        text="Ниже кнопки. Нажмите на необходимую для изменения информации.",
        reply_markup=game_counter(_buttons)
    )


@router.callback_query(F.data == "button_game_duration")
async def button_game_duration_handler(call: CallbackQuery, state: FSMContext):
    await state.update_data(button_2="button_game_duration")
    await call.message.delete()
    await call.message.answer(
        text="Введите длительность в минутах (60 / 90 / 120)",
        reply_markup=durations()
    )
    await state.set_state(CalculatorStates.waiting_for_duration)
    await call.answer()


@router.message(CalculatorStates.waiting_for_duration)
async def process_input(message: Message, state: FSMContext):
    duration = message.text

    data = await state.get_data()
    _buttons = data.get("buttons")
    button_id = data.get("button_2")
    _buttons[button_id] = f"🕒 Длительность игры: {duration} мин."
    await state.update_data(buttons=_buttons)

    await message.answer(
        text="Ниже кнопки. Нажмите на необходимую для изменения информации.",
        reply_markup=game_counter(_buttons)
    )


@router.callback_query(F.data == "button_range")
async def button_game_duration_handler(call: CallbackQuery, state: FSMContext):
    await state.update_data(button_3="button_range")
    await call.message.edit_text(
        text="Введите сумму за дальность (например: 25000)",
        reply_markup=return_button()
    )
    await state.set_state(CalculatorStates.waiting_for_range_value)
    await call.answer()


@router.message(CalculatorStates.waiting_for_range_value)
async def process_input(message: Message, state: FSMContext):
    range_value = message.text

    try:
        range_value = int(range_value)
    except ValueError:
        await message.answer("Неверные данные.")

    data = await state.get_data()
    _buttons = data.get("buttons")
    button_id = data.get("button_3")
    _buttons[button_id] = f"📍 Доплата за дальность: {"{:,.0f}".format(range_value).replace(',', '.')}"
    await state.update_data(buttons=_buttons)

    await message.answer(
        text="Ниже кнопки. Нажмите на необходимую для изменения информации.",
        reply_markup=game_counter(_buttons)
    )


@router.callback_query(F.data == "button_percentage_discount")
async def button_game_duration_handler(call: CallbackQuery, state: FSMContext):
    await state.update_data(button_4="button_percentage_discount")
    await call.message.edit_text(
        text="Введите скидку в процентах (просто числом без знака)",
        reply_markup=return_button()
    )
    await state.set_state(CalculatorStates.waiting_for_percentage_discount)
    await call.answer()


@router.message(CalculatorStates.waiting_for_percentage_discount)
async def process_input(message: Message, state: FSMContext):
    discount = message.text

    try:
        discount = int(discount)
    except ValueError:
        await message.answer('Неверное значение.')

    data = await state.get_data()
    _buttons = data.get("buttons")
    button_id = data.get("button_4")
    _buttons[button_id] = f"📉 Скидка в процентах: {discount}%"
    await state.update_data(buttons=_buttons)

    await message.answer(
        text="Ниже кнопки. Нажмите на необходимую для изменения информации.",
        reply_markup=game_counter(_buttons)
    )


@router.callback_query(F.data == "button_numerical_discount")
async def button_game_duration_handler(call: CallbackQuery, state: FSMContext):
    await state.update_data(button_5="button_numerical_discount")
    await call.message.edit_text(
        text="Введите скидку в сумме (например: 5000)",
        reply_markup=return_button()
    )
    await state.set_state(CalculatorStates.waiting_for_numerical_discount)
    await call.answer()


@router.message(CalculatorStates.waiting_for_numerical_discount)
async def process_input(message: Message, state: FSMContext):
    discount = message.text

    try:
        discount = int(discount)
    except ValueError:
        await message.answer(text='Это не число!')
    data = await state.get_data()
    _buttons = data.get("buttons")
    button_id = data.get("button_5")
    _buttons[button_id] = f"💸 Скидка в сумме: {"{:,.0f}".format(discount).replace(',', '.')}"
    await state.update_data(buttons=_buttons)

    await message.answer(
        text="Ниже кнопки. Нажмите на необходимую для изменения информации.",
        reply_markup=game_counter(_buttons)
    )


@router.callback_query(F.data == "button_do_nothing")
async def button_do_nothing_handler(call: CallbackQuery):
    await call.answer(text="Чуть-чуть промахнулся кнопкой", show_alert=False)


@router.callback_query(F.data == "button_prepayment")
async def button_prepayment_handler(call: CallbackQuery):
    await call.message.edit_text(
        text="Выберите сумму предоплаты",
        reply_markup=prepayment_button()
    )


@router.callback_query(F.data.in_({"button_5000", "button_25000"}))
async def button_prepayment_handler(call: CallbackQuery, state: FSMContext):
    await state.update_data(button_5000="button_5000", button_25000="button_25000")
    data = await state.get_data()
    _buttons = data.get("buttons")
    button_id = data.get("button_5000")

    if call.data == "button_5000":
        await state.update_data(button_prepayment_sum="button_prepayment")
        data = await state.get_data()
        _buttons = data.get("buttons")
        button_id = data.get("button_prepayment_sum")
        _buttons[button_id] = f"💳 Предоплата: 5.000"
        await state.update_data(buttons=_buttons)
    elif call.data == "button_25000":
        await state.update_data(button_prepayment_sum="button_prepayment")
        data = await state.get_data()
        _buttons = data.get("buttons")
        button_id = data.get("button_prepayment_sum")
        _buttons[button_id] = f"💳 Предоплата: 25.000"
        await state.update_data(buttons=_buttons)

    await call.message.edit_text(
        text="Ниже кнопки. Нажмите на необходимую для изменения информации.",
        reply_markup=game_counter(_buttons)
    )


@router.callback_query(F.data == "button_done")
async def button_game_duration_handler(call: CallbackQuery, state: FSMContext):
    await state.update_data(button_done="button_done")

    buttons_data = await state.get_data()
    buttons = buttons_data.get("buttons")

    guests_amount = int(parse_value(buttons.get("button_guests_amount"), "Количество участников"))
    game_duration = int(parse_value(buttons.get("button_game_duration"), "Длительность игры"))
    range_value = parse_value(buttons.get("button_range"), "Доплата за дальность")
    percentage_discount = int(
        parse_value(buttons.get("button_percentage_discount"), "Скидка в процентах")) if parse_value(
        buttons.get("button_percentage_discount"), "Скидка в процентах") is not None else None
    numerical_discount = parse_value(buttons.get("button_numerical_discount"), "Скидка в сумме")
    prepayment = parse_value(buttons.get("button_prepayment"), "Предоплата")

    msg = detailed_count_game_sum(guests_amount, game_duration, range_value,
                                  percentage_discount, numerical_discount, prepayment)
    total_sum = int(count_game_sum(guests_amount, game_duration, range_value,
                                   percentage_discount, numerical_discount, prepayment))

    await call.message.edit_text(
        text=f"{msg}\n\n<b>Итоговая сумма:</b> {total_sum:,}".replace(",", ".")
    )

    await state.clear()
