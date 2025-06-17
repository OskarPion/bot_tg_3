from .handlers import router
from .request_router import request_router
from .jobs_prog_router import jobs_router
from aiogram import Dispatcher
from .photo_video_router import photo_video_router
from .document_router import document_router
from .voice_router import voice_router


def register_routers(dp: Dispatcher):
    dp.include_routers(router, request_router, photo_video_router, document_router, voice_router,jobs_router)
