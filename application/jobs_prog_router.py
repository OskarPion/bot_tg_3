from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.states import JobsStates

import application.keyboards as kb


jobs_router = Router()


@jobs_router.callback_query(F.data == "catalog")
async def jobs_buttons(callback: CallbackQuery):
    await callback.message.edit_text("Отправьте фронт или бек", reply_markup=kb.jobs())


@jobs_router.callback_query(F.data == "frontend")
async def frontend_button(callback: CallbackQuery):
    await callback.message.answer("Отправьте вашу классификацию", reply_markup=None)


@jobs_router.callback_query(F.data == "backend")
async def backend_button(callback: CallbackQuery):
    await callback.message.answer("Отправьте вашу классификацию", reply_markup=None)


@jobs_router.message()
async def done_jobs(message: Message):
    await message.answer("Спасибо, мы вам перезвоним")
