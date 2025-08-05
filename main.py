from aiogram import Bot, Dispatcher

import asyncio
import logging

from src.handlers.admin.notifications import router as notifications_router
from src.handlers.registration import router as registration_router
from src.handlers.admin.gallery import router as gallery_router
from src.handlers.fallback import router as fallback_router
from src.handlers.admin.main import router as admin_router
from src.handlers.admin.vote import router as vote_router
from src.handlers.menu import router as menu_router
from config import settings


async def main() -> None:
    bot = Bot(token=settings.TOKEN)
    dp = Dispatcher()
    dp.include_routers(admin_router,
                       gallery_router,
                       notifications_router,
                       vote_router,
                       registration_router,
                       menu_router,
                       fallback_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('[EXIT]')
