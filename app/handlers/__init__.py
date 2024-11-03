from aiogram import Router
from .main import router as start_router
from .calculator import router as calculator_router
from .certificate import router as certificate_router
from .admin.employees import router as admin_router

main_router = Router()
main_router.include_routers(start_router, calculator_router, certificate_router, admin_router)
