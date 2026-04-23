import asyncio

from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class SlowMiddleware(BaseMiddleware):
    def __init__(self, delay: int):
        self.delay = delay

    async def __call__(
            self, 
            handler: Callable[[TelegramObject, Dict], Awaitable[Any]], 
            event: TelegramObject, 
            data: Dict[str, Any]
    ) -> Any:
        await asyncio.sleep(self.delay)
        result = await handler(event, data)
        print(f"Хендлер спал: {self.delay} секунд")
        return result