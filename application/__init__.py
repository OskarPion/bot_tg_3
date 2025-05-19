from .handlers import router
from .request_router import request_router
from .jobs_prog_router import jobs_router
from aiogram import Dispatcher


def register_routers(dp: Dispatcher):
    dp.include_routers(router, request_router, jobs_router)
