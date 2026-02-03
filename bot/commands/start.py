from aiogram import types
from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder, ReplyKeyboardMarkup,
    InlineKeyboardBuilder, InlineKeyboardMarkup,
    InlineKeyboardButton, KeyboardButton, KeyboardButtonPollType
)


async def about_me(message: types.Message) -> None:
    aboutme_board = InlineKeyboardBuilder()

    links = [
        ("YouTube", "https://www.youtube.com/@asurbeats"),
        ("Twitch", "https://www.twitch.tv/asurbeats"),
        ("Boosty", "https://boosty.to/asurbeats"),
        ("TikTok", "https://www.tiktok.com/@zero.saiky?_r=1&_t=ZP-93cGbrif18J"),
        ("YT(Games)", "https://www.youtube.com/@zerosaiky"),
    ]

    for text, url in links:
        aboutme_board.button(text=text, url=url)

    await message.answer_photo(
        photo='https://images.boosty.to/image/f3057592-3146-498c-b3f9-d136514d6968?change_time=1768563977',
        caption='🎧 Мои соцсети',
        reply_markup=aboutme_board.as_markup()
    )


async def faq(message: types.Message) -> None:
    pass

async def start_command(message: types.Message) -> None:
    menu_builder = ReplyKeyboardBuilder()
    buttons = ["📢 РАССЫЛКА", "🎵 МОИ СОЦСЕТИ", "👤 FAQ"]
    for button in buttons:
        menu_builder.add(types.KeyboardButton(text=button))
    menu_builder.adjust(1)

    await message.answer(
    "Привет! Я бот Асура.\n"
        "Выбирай что интересует:",
        reply_markup=menu_builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=False
        )
    )