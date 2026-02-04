__all__ = ['start', 'register_user_commands']

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram import F

from bot.commands.start import (start_command, about_me, faq, newsletter,
                                show_subscription_success, back_to_list)


def register_user_commands(router: Router) -> None:
    router.message.register(start_command, CommandStart())
    router.message.register(about_me, F.text == '🎵 МОИ СОЦСЕТИ')
    router.message.register(faq, F.text == '👤 FAQ')
    router.message.register(newsletter, F.text == '📢 РАССЫЛКА')

    router.callback_query.register(show_subscription_success, F.data.startswith("sub_"))
    router.callback_query.register(back_to_list, F.data == "back_to_subs")

