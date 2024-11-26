from aiogram import Router
from .main import router as start_router
from .calculator import router as calculator_router
from .certificate import router as certificate_router
from .penalties import router as penalty_router
from .my_profile import router as profile_router
from .admin import router as admin_router
from .barrier import router as barrier_router

main_router = Router()
main_router.include_routers(start_router,
                            calculator_router,
                            certificate_router,
                            admin_router,
                            penalty_router,
                            profile_router,
                            barrier_router
                            )
