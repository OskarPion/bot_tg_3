from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from services.image_search import search_image

import application.keyboards as kb

photo_router = Router()


@photo_router.message(F.text.startswith("/photo"))
async def handle_photo_request(message: Message):
    query = message.text.replace("/photo", "").strip()
    if not query:
        await message.reply("Укажите запрос после /photo")
        return

    try:
        image_url = await search_image(query)
        if image_url:
            await message.reply_photo(image_url, caption=f"Результат: {query}")
        else:
            await message.reply("Изображение не найдено")
    except Exception as e:
        await message.reply(f"Ошибка: {str(e)}")
