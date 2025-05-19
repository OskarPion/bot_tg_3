from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.states import JobsStates

import application.keyboards as kb


jobs_router = Router()


@jobs_router.callback_query(F.data == "catalog")
async def front_jobs(callback: CallbackQuery, state: FSMContext):
    await state.set_state(JobsStates.jobs_name)
    await callback.message.answer("Отправьте фронт или бек")


@jobs_router.message(JobsStates.jobs_name)
async def send_classifacation(message: Message, state: FSMContext):
    await state.set_state(JobsStates.classification)
    await message.answer("Отправьте вашу классификацию")


@jobs_router.message(JobsStates.classification)
async def money(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Спасибо за заявку!", reply_markup=kb.menu_keyboard())
