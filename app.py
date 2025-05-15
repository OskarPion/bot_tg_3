import asyncio
from contextlib import asynccontextmanager
import aiogram

from config.logger import logger

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, Update
from fastapi import FastAPI
from config import TOKEN, DOMAIN, WEBHOOK_PATH, WEBHOOK_URL

from application.handlers import router as handlers_router


def print_registered_handlers(router):
    # Для сообщений
    print("Message handlers:")
    for handler in router.message.handlers:
        print(f"- Handler: {handler.callback.__name__}")
        print(f"  Filters: {handler.filters}")

    # Для callback-запросов
    print("\nCallback handlers:")
    for handler in router.callback_query.handlers:
        print(f"- Handler: {handler.callback.__name__}")
        print(f"  Filters: {handler.filters}")


bot = Bot(token=TOKEN)
dp = Dispatcher()


async def check_and_update_webhook(bot: Bot):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)
        logger.info(f"Webhook updated to {WEBHOOK_URL}")
    else:
        logger.info(f"Webhook is {WEBHOOK_URL}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    dp.include_router(handlers_router)
    asyncio.create_task(check_and_update_webhook(bot))
    print_registered_handlers(handlers_router)
    logger.info("App started")
    # await start_messages()
    yield
    await bot.session.close()
    logger.info("App stopped")


app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def get_update(data: dict):
    try:
        update = Update(**data)
        await dp.feed_update(bot, update)
    except Exception as e:
        logger.error(e, exc_info=True)
