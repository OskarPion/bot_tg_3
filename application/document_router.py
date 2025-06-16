from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.states import DocumentStates

import application.keyboards as kb

document_router = Router()

@document_router.callback_query(F.data == 'send_file')
async def send_file_from_user(callback:CallbackQuery, state: FSMContext):
    await state.set_state(DocumentStates.document)
    await callback.message.answer("Пришлите файл")

@document_router.message(DocumentStates.document, F.document)
async def handle_document(message: Message, state: FSMContext):
    document = message.document
    file_id = document.file_id
    file_name = document.file_name

    await message.answer(f"Файл получен! Имя: {file_name}")
    await state.clear()


@document_router.message(DocumentStates.document)
async def wrong_document_format(message: Message):
    await message.answer("Пожалуйста, отправьте файл (не фото/видео)")



