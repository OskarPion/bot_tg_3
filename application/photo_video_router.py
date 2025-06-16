from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.states import PhotoStates


import application.keyboards as kb

photo_video_router = Router()


@photo_video_router.callback_query(F.data == "send_photo")
async def send_photo(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PhotoStates.send_photo)
    await callback.message.answer("Пришлите фото")


@photo_video_router.callback_query(F.data == "send_video")
async def send_video(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PhotoStates.send_video)
    await callback.message.answer("Пришлите видео")

@photo_video_router.message(PhotoStates.send_photo, F.photo)
async def handle_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]  
    file_id = photo.file_id
    await message.answer(f"Фото получено! file_id: {file_id}", reply_markup = kb.photo_video_keyboard())
    await state.clear()

@photo_video_router.message(PhotoStates.send_video, F.video)
async def handle_video(message: Message, state: FSMContext):
    video = message.video
    file_id = video.file_id
    await message.answer(f"Видео получено! file_id: {file_id}", reply_markup = kb.photo_video_keyboard())
    await state.clear()
