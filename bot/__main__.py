import asyncio
import logging
import os
import sys

from aiogram import Dispatcher, Bot, Router
from aiogram.fsm.storage.memory import MemoryStorage

from bot.database import Database
from bot.middlewares.db import DatabaseMiddleware

from handlers import register_admin_commands
from commands import register_user_commands


async def main() -> None:
    db = Database()
    bot = Bot(token=os.getenv('token'))
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(DatabaseMiddleware(db))
    dp.callback_query.middleware(DatabaseMiddleware(db))

    user_router = Router(name="user")
    register_user_commands(user_router)
    dp.include_router(user_router)

    admin_router = Router(name="admin")
    register_admin_commands(admin_router)
    dp.include_router(admin_router)

    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s',
        handlers=[
            logging.FileHandler('bot.log'),
            logging.StreamHandler(sys.stdout)  # консоль
        ]
    )
    logger = logging.getLogger(__name__)
    try:
        logger.info('Starting bot...')
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
