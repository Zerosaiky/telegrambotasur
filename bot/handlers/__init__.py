__all__ = ['admin', 'register_admin_commands']

from aiogram import Router
from aiogram.filters import Command

from bot.handlers.admin import (start_broadcast, get_category, send_broadcast, BroadcastForm)


def register_admin_commands(router: Router) -> None:
    router.message.register(start_broadcast, Command("broadcast"))
    router.message.register(get_category, BroadcastForm.category)
    router.message.register(send_broadcast, BroadcastForm.message)

