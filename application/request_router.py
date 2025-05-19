from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.states import RequestStates, JobsStates

import application.keyboards as kb


request_router = Router()


@request_router.callback_query(F.data == "request")
async def send_request(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RequestStates.name)
    await callback.message.answer("Пришлите ваше ФИО")


@request_router.message(RequestStates.name)
async def send_description(message: Message, state: FSMContext):
    await state.set_state(RequestStates.description)
    await message.answer("Отправьте описание заявки")


@request_router.message(RequestStates.description)
async def send_email(message: Message, state: FSMContext):
    await state.set_state(RequestStates.email)
    await message.answer("Отправьте email ")


@request_router.message(RequestStates.email)
async def validate_email(message: Message, state: FSMContext):
    if "@" not in message.text:
        return await message.answer("Неправильный email")
    await state.clear()
    await message.answer("Заявка отправлена", reply_markup=kb.menu_keyboard())
