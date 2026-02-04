import asyncio
import logging
import os
import sys

from aiogram import Dispatcher, Bot
from commands import register_user_commands
from bot.database import Database
from bot.middlewares.db import DatabaseMiddleware

async def main() -> None:
    db = Database()
    dp = Dispatcher()
    bot = Bot(token=os.getenv('token'))
    dp.message.middleware(DatabaseMiddleware(db))
    dp.callback_query.middleware(DatabaseMiddleware(db))

    register_user_commands(dp)
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
