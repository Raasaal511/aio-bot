from aiogram import BaseMiddleware

from aiogram.types import Update


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        print(f"Processing update: {event}")
        return await handler(event, data)
