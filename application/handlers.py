from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from config.logger import logger

import application.keyboards as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет!", reply_markup=kb.menu_keyboard())


@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer("Это команда /help")


@router.message(F.text == "Как дела?")
async def how_are_you(message: Message):
    await message.answer("Gut")


@router.callback_query(F.data == "catalog")
async def catalog_button(callback: CallbackQuery):
    await callback.message.answer("Это будет каталог", reply_markup=kb.menu_keyboard())
