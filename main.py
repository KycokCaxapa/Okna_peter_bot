from aiogram import Bot, Dispatcher

import asyncio
import logging

from src.handlers.registration import router as registration_router
from src.handlers.menu import router as menu_router
from config import settings


async def main() -> None:
    bot = Bot(token=settings.TOKEN)
    dp = Dispatcher()
    dp.include_routers(registration_router,
                       menu_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('[EXIT]')
