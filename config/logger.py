import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_PATH = LOG_DIR / "bot.log"


file_handler = RotatingFileHandler(
    filename=LOG_PATH,
    mode="a+",
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)

console_handler = logging.StreamHandler()

logger = logging.getLogger("bot")
logging.basicConfig(
    handlers=(file_handler, console_handler),
    level=logging.DEBUG,
    format="%(asctime)s %(filename)s:%(lineno)d #%(levelname)-4s %(name)s: %(message)s",
)
