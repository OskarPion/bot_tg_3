import asyncio
from contextlib import asynccontextmanager
import aiogram

from config.logger import logger

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, Update
from fastapi import FastAPI
from config import TOKEN, DOMAIN, WEBHOOK_PATH, WEBHOOK_URL

from aiogram.fsm.storage.memory import MemoryStorage

from application import register_routers
from db.connection import connect_to_db, disconnect_from_db
from middlewares.rate_limit import RateLimitMiddleware


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.message.middleware(RateLimitMiddleware(delay=2.0))


async def check_and_update_webhook(bot: Bot):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)
        logger.info(f"Webhook updated to {WEBHOOK_URL}")
    else:
        logger.info(f"Webhook is {WEBHOOK_URL}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_db()
    register_routers(dp)
    asyncio.create_task(check_and_update_webhook(bot))
    logger.info("App started")
    # await start_messages()
    yield
    await disconnect_from_db()
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
