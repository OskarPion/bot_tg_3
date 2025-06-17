import os
import json
import wave
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer
from uuid import uuid4

voice_router = Router()
logger = logging.getLogger(__name__)

# Инициализация модели при старте (лучше чем lazy loading)
model_path = os.path.join(os.path.dirname(__file__), "vosk-model-small-ru-0.22")
try:
    model = Model(model_path)
    logger.info("Модель Vosk успешно загружена")
except Exception as e:
    logger.error(f"Ошибка загрузки модели Vosk: {e}")
    model = None

@voice_router.message(F.voice)
async def handle_voice_message(message: Message, bot: Bot):
    if model is None:
        await message.reply("Система распознавания голоса временно недоступна")
        return

    logger.info(f"Получено голосовое сообщение от {message.from_user.id}")

    ogg_path = None
    wav_path = None

    try:
        # Скачивание файла
        file_info = await bot.get_file(message.voice.file_id)
        voice_data = await bot.download_file(file_info.file_path)

        # Создание временных файлов
        ogg_path = f"temp_{uuid4().hex}.ogg"
        wav_path = f"temp_{uuid4().hex}.wav"

        # Сохранение OGG
        with open(ogg_path, "wb") as f:
            f.write(voice_data.getvalue())

        # Конвертация в WAV
        audio = AudioSegment.from_ogg(ogg_path)
        audio.export(wav_path, format="wav", codec="pcm_s16le")  # Явно указываем параметры

        # Распознавание
        wf = wave.open(wav_path, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
            raise ValueError("Аудиофайл должен быть моно (1 канал) и 16 бит на сэмпл")

        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)

        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                part_result = json.loads(rec.Result())
                results.append(part_result.get("text", ""))

        final_result = json.loads(rec.FinalResult())
        results.append(final_result.get("text", ""))

        text = " ".join(filter(None, results))  # Фильтруем пустые строки
        
        if text.strip():
            await message.reply(f"Распознанный текст: {text}")
        else:
            await message.reply("Не удалось распознать текст. Возможно, сообщение слишком короткое или неразборчивое.")

    except Exception as e:
        logger.exception(f"Ошибка при обработке голосового сообщения: {e}")
        await message.reply(f"Произошла ошибка при обработке голосового сообщения: {str(e)}")

    finally:
        # Удаление временных файлов
        for path in [ogg_path, wav_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as e:
                    logger.error(f"Ошибка при удалении {path}: {e}")