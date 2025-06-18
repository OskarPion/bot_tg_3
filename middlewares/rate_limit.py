import time
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from typing import Callable, Awaitable, Dict, Any
from collections import defaultdict

class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, delay: float = 2.0):
        self.delay = delay  # время между сообщениями
        self.last_time: Dict[int, float] = defaultdict(float)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id
            now = time.time()
            elapsed = now - self.last_time[user_id]

            if elapsed < self.delay:
                await event.answer("⏱ Пожалуйста, не так быстро!")
                return  # Не вызываем handler — блокируем
            else:
                self.last_time[user_id] = now

        return await handler(event, data)
