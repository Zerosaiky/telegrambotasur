import asyncio
import logging
import os
import sys

from aiogram import Dispatcher, Bot, Router
from aiogram.fsm.storage.memory import MemoryStorage

from bot.database import Database
from bot.middlewares.db import DatabaseMiddleware

from bot.handlers import register_admin_commands
from bot.commands import register_user_commands


async def main() -> None:
    db = Database()

    admin_ids_str = os.getenv("ADMIN_IDS", "")
    if admin_ids_str:
        try:
            admin_ids = [
                int(uid.strip())
                for uid in admin_ids_str.split(",")
                if uid.strip().isdigit()
            ]

            added = []
            for uid in admin_ids:
                if not db.is_admin(uid):
                    db.add_admin(uid)
                    added.append(uid)

            if added:
                logger.info(f"Автоматически добавлены новые админы: {added}")
            else:
                logger.info("Все указанные админы уже есть в базе")

        except ValueError as e:
            logger.error(f"Ошибка в ADMIN_IDS: некорректные ID → {e}")
    else:
        logger.warning("ADMIN_IDS не указан в .env — админы не добавлены автоматически")

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

