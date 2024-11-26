from aiogram import Router, F
from aiogram.types import CallbackQuery

from .barrier import router as barrier_router
from .employees import router as employees_router
from ...keyboards.inline_kbs import admin_panel_kb

router = Router()
router.include_routers(employees_router, barrier_router)


@router.callback_query(F.data == "admin_panel")
async def admin_panel(call: CallbackQuery):
    await call.message.edit_text(
        text=f"Добро пожаловать, {call.from_user.full_name}!",
        reply_markup=admin_panel_kb()
    )
