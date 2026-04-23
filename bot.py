import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import bot_settings
from db import init_db
from routers import router as main_router
from middlewares.logging import LoggingMiddleware


async def main():
    # logging.basicConfig(
    # level=logging.INFO,
    # format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    # )
    bot = Bot(token=bot_settings.TOKEN)
    dp = Dispatcher()

    await init_db()

    dp.include_router(main_router)
    dp.update.middleware(LoggingMiddleware())

    logging.info("Бот запущен")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())