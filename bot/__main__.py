import asyncio
import logging
import os
import sys

from aiogram import Dispatcher, Bot
from commands import register_user_commands

async def main() -> None:
    dp = Dispatcher()
    bot = Bot(token=os.getenv('token'))

    register_user_commands(dp)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s',
            handlers=[
                logging.FileHandler('bot.log'),
                logging.StreamHandler(sys.stdout) #консоль
            ]
        )
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")
