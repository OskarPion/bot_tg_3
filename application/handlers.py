from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import datetime
import requests

from config.logger import logger

from services.weather import get_weather

import application.keyboards as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет!", reply_markup=kb.photo_video_keyboard())


@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer("Это команда /help")


@router.message(F.text == "Как дела?")
async def how_are_you(message: Message):
    await message.answer("Gut")


@router.callback_query(F.data == "news")
async def news_button(callback: CallbackQuery):
    await callback.message.answer("news")

@router.message(Command("weather"))
async def weather_cmd(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Введите город после команды, например:\n/weather Казань")
        return

    city = parts[1]
    logger.info(f"Пользователь {message.from_user.id} запросил погоду для {city}")
    weather_info = await get_weather(city)
    await message.answer(weather_info)
