from datetime import date, datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Router, F

from app.database import create_certificate, is_used_certificate
from app.keyboards.inline_kbs import certificates_kb, main_kb, certificates_sum_kb, \
    certificate_date_for_5k_kb, certificate_date_for_10k_kb
from app.methods import draw_5k, draw_10k, is_valid_date
from app.states import CertificateStates

router = Router()


@router.callback_query(F.data == "certificates")
async def certificate_start_handler(call: CallbackQuery):
    await call.message.edit_text("Что хотите сделать?", reply_markup=certificates_kb())


@router.callback_query(F.data == "to_main_menu")
async def to_main_menu_handler(call: CallbackQuery):
    await call.message.edit_text(
        text="На стадии разработки...",
        reply_markup=await main_kb(call.from_user.id)
    )


@router.callback_query(F.data == "back_to_cert_menu")
async def back_to_cert_menu_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(text="Что хотите сделать?", reply_markup=certificates_kb())


@router.callback_query(F.data == "create_new_cert")
async def create_new_cert_handler(call: CallbackQuery):
    await call.message.edit_text(text="Выберите сумму сертификата",
                                 reply_markup=certificates_sum_kb())


@router.callback_query(F.data == "cert_5k")
async def cert_5k_handler(call: CallbackQuery):
    await call.message.edit_text(text="Выберите дату для сертификата",
                                 reply_markup=certificate_date_for_5k_kb())


@router.callback_query(F.data == "cert_10k")
async def cert_10k_handler(call: CallbackQuery):
    await call.message.edit_text(text="Выберите дату для сертификата",
                                 reply_markup=certificate_date_for_10k_kb())


@router.callback_query(F.data == "current_date_for_5k")
async def current_date_handler(call: CallbackQuery):
    current_date = date.today().strftime("%Y-%m-%d")
    cert_id, date_of_cert = await create_certificate(current_date)
    output_path = draw_5k(date_of_cert, cert_id)
    await call.message.delete()
    await call.message.answer_document(document=FSInputFile(path=output_path),
                                       caption="Ваш сертификат готов!")
    await call.message.answer(text="На стадии разработки...",
                              reply_markup=await main_kb(call.from_user.id))


@router.callback_query(F.data == "date_from_user_for_5k")
async def date_from_user_for_5k_handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Введите дату в формате <b>ГГГГ-ММ-ДД</b>\n"
                                      "(например: <b>2011-09-11</b>)")
    await state.set_state(CertificateStates.date_from_user_5k)


@router.message(CertificateStates.date_from_user_5k)
async def date_from_user_for_5k_handler_(message: Message, state: FSMContext):
    user_date = message.text

    if not is_valid_date(user_date):
        await message.answer("<b>Неправильная дата!</b>\n"
                             "Введите дату в формате <b>ГГГГ-ММ-ДД</b>\n"
                             "(например: <b>2011-09-11</b>)")

    formatted_date = datetime.strptime(user_date, '%Y-%m-%d').date()

    await message.delete()

    cert_id, date_of_cert = await create_certificate(formatted_date)
    output_path = draw_5k(user_date, cert_id)

    await message.answer_document(document=FSInputFile(path=output_path),
                                  caption="Ваш сертификат готов!")
    await message.answer(text="На стадии разработки...",
                         reply_markup=await main_kb(message.from_user.id))

    await state.clear()


@router.callback_query(F.data == "current_date_for_10k")
async def current_date_handler(call: CallbackQuery):
    current_date = date.today().strftime("%Y-%m-%d")
    cert_id, date_of_cert = await create_certificate(current_date)
    output_path = draw_10k(date_of_cert, cert_id)
    await call.message.delete()
    await call.message.answer_document(document=FSInputFile(path=output_path),
                                       caption="Ваш сертификат готов!")
    await call.message.answer(text="На стадии разработки...",
                              reply_markup=await main_kb(call.from_user.id))


@router.callback_query(F.data == "date_from_user_for_10k")
async def date_from_user_for_10k_handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Введите дату в формате <b>ГГГГ-ММ-ДД</b>\n"
                                      "(например: <b>2011-09-11</b>)")
    await state.set_state(CertificateStates.date_from_user_10k)


@router.message(CertificateStates.date_from_user_10k)
async def date_from_user_for_10k_handler_(message: Message, state: FSMContext):
    user_date = message.text

    if not is_valid_date(user_date):
        await message.answer("<b>Неправильная дата!</b>\n"
                             "Введите дату в формате <b>ГГГГ-ММ-ДД</b>\n"
                             "(например: <b>2011-09-11</b>)")

    formatted_date = datetime.strptime(user_date, '%Y-%m-%d').date()

    await message.delete()

    cert_id, date_of_cert = await create_certificate(formatted_date)
    output_path = draw_10k(user_date, cert_id)

    await message.answer_document(document=FSInputFile(path=output_path),
                                  caption="Ваш сертификат готов!")
    await message.answer(text="На стадии разработки...",
                         reply_markup=await main_kb(message.from_user.id))

    await state.clear()


@router.callback_query(F.data == "check_cert")
async def check_certificate_handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text='Введите номер сертификата (то, что <b>после "Online-"</b>')
    await state.set_state(CertificateStates.id_of_certificate)


@router.message(CertificateStates.id_of_certificate)
async def check_certificate_handler_(message: Message, state: FSMContext):
    id_of_cert = int(message.text)

    if await is_used_certificate(id_of_cert):
        await message.answer(f"Сертификат с номером <b>{id_of_cert}</b> не существует или уже был использован.")
        await message.answer(f"Главное меню", reply_markup=await main_kb(message.from_user.id))
    else:
        await message.answer(f"Сертификат с номером <b>{id_of_cert}</b> не был использован.")
        await message.answer("Главное меню", reply_markup=await main_kb(message.from_user.id))
    await state.clear()
