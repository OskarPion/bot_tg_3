from config.logger import logger
from .database import database, metadata
from sqlalchemy import create_engine
from config.settings import DB_URL


# создаём sync engine для create_all
sync_engine = create_engine(DB_URL.replace("+asyncpg", ""))  # без asyncpg


async def connect_to_db():
    try:
        await database.connect()
        logger.info("Database connected successfully")

        # create tables (если не существуют)
        metadata.create_all(sync_engine)
        logger.info("Database tables created")
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise


async def disconnect_from_db():
    try:
        await database.disconnect()
        logger.info("Database disconnected successfully")
    except Exception as e:
        logger.error(f"Database disconnection error: {e}")
