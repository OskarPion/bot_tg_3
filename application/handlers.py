from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ContentType, FSInputFile
from PIL import Image, ImageDraw, ImageFont
import io
import os
import tempfile
import datetime
import requests

from config.logger import logger
from services.weather import get_weather
import application.keyboards as kb

router = Router()

# Путь к шрифту (замените на существующий шрифт в вашей системе)
FONT_PATH = "arial.ttf"
FONT_SIZE = 40


async def process_image(caption: str) -> Image.Image:
    """Создает изображение с текстом из подписи."""
    try:
        # Создаем новое белое изображение
        width, height = 800, 400
        new_image = Image.new("RGB", (width, height), color="white")
        draw = ImageDraw.Draw(new_image)

        try:
            font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        except:
            logger.warning("Шрифт не найден, используется шрифт по умолчанию")
            font = ImageFont.load_default()

        # Очищаем текст от лишних символов
        text = caption.strip() if caption else ""
        if not text:
            logger.info("Подпись к фото отсутствует")
            return None

        # Вычисляем размеры текста
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Центрируем текст
        text_x = (width - text_width) // 2
        text_y = (height - text_height) // 2

        # Рисуем текст
        draw.text((text_x, text_y), text, font=font, fill="black")

        return new_image
    except Exception as e:
        logger.error(f"Ошибка обработки изображения: {str(e)}")
        return None


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Отправь фото с подписью, и я верну изображение с этим текстом!",
        reply_markup=kb.photo_video_keyboard(),
    )


@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer("Это команда /help")


@router.message(F.text == "Как дела?")
async def how_are_you(message: Message):
    await message.answer("Gut")


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


@router.message(F.content_type == ContentType.PHOTO)
async def handle_photo(message: Message):
    """Обрабатывает полученное фото, добавляет текст из подписи по центру и отправляет обратно"""
    try:
        logger.info(f"Пользователь {message.from_user.id} отправил фото")

        # Получаем текст из подписи
        caption = message.caption
        if not caption:
            await message.reply("Пожалуйста, добавьте подпись к фото.")
            return

        # Скачиваем фото (наилучшего качества)
        photo = message.photo[-1]
        file_id = photo.file_id
        file = await message.bot.get_file(file_id)
        file_bytes = await message.bot.download_file(file.file_path)

        # Открываем исходное изображение
        original_image = Image.open(io.BytesIO(file_bytes.read()))
        draw = ImageDraw.Draw(original_image)
        text = caption.strip()

        # Установим значения по умолчанию
        font_size = 40
        text_width = original_image.width * 0.8  # 80% ширины изображения
        text_height = font_size

        try:
            # Пробуем загрузить шрифт
            try:
                font = ImageFont.truetype(FONT_PATH, font_size)
            except:
                logger.warning("Шрифт не найден, используется шрифт по умолчанию")
                font = ImageFont.load_default()

            # Рассчитываем размеры текста
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # Автоподбор размера шрифта
            while text_width > original_image.width * 0.9 and font_size > 20:
                font_size -= 5
                try:
                    font = ImageFont.truetype(FONT_PATH, font_size)
                    text_bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                except:
                    continue

        except Exception as font_error:
            logger.error(f"Ошибка при работе со шрифтом: {font_error}")
            font = ImageFont.load_default()
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

        # Позиция текста (по центру)
        text_x = (original_image.width - text_width) // 2
        text_y = (original_image.height - text_height) // 2

        # Добавляем полупрозрачный фон под текст
        background = Image.new("RGBA", original_image.size, (0, 0, 0, 0))
        draw_bg = ImageDraw.Draw(background)
        draw_bg.rectangle(
            [
                text_x - 20,
                text_y - 10,
                text_x + text_width + 20,
                text_y + text_height + 10,
            ],
            fill=(0, 0, 0, 150),  # Полупрозрачный черный
        )

        # Комбинируем изображения
        original_image.paste(
            Image.alpha_composite(original_image.convert("RGBA"), background), (0, 0)
        )

        # Рисуем белый текст
        draw.text((text_x, text_y), text, font=font, fill="white")

        # Сохраняем результат
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            original_image.save(tmp_file.name, format="PNG")
            await message.reply_photo(
                photo=FSInputFile(tmp_file.name), caption="Вот ваше фото с текстом!"
            )
            os.unlink(tmp_file.name)

    except Exception as e:
        logger.error(f"Ошибка при обработке фото: {str(e)}")
        await message.reply(f"Произошла ошибка: {str(e)}")
