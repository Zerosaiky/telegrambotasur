from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder, InlineKeyboardBuilder
)


async def handle_subscription(call: types.CallbackQuery, db):
    user_id = call.from_user.id
    category = call.data[4:]
    new_status = db.toggle_subscription(user_id, category)
    if new_status:
        await call.answer(f"✅ Подписан на: {new_status}")
    else:
        await call.answer(f"❌ Отписан от: {category}")


async def newsletter(message: types.Message, db) -> None:
    user_id = message.from_user.id
    current = db.get_subscription(user_id)

    type_content = InlineKeyboardBuilder()

    contents = [
        ("Биты", "sub_beats", "beats"),
        ("Трансляции по музыке", "sub_music_streams", "music_streams"),
        ("Только музыкальный контент", "sub_music_only", "music_only"),
        ("Игры", "sub_games", "games"),
        ("Весь контент", "sub_all", "all"),
    ]

    for text, callback_data, sub_key in contents:
        is_active = (current == sub_key)
        status = "✅" if is_active else "❌"
        button_text = f"{status} {text}"

        type_content.button(text=button_text, callback_data=callback_data)

    type_content.adjust(1)

    status_text = f"Текущая подписка: <b>{current}</b>" if current else "Нет активной подписки"

    await message.answer(
        "📢 <b>Управление подписками</b>\n\n"
        f"{status_text}\n\n"
        "✅ — Текущая подписка\n"
        "❌ — Можно подписаться\n\n"
        "<i>Нажми на кнопку чтобы переключить</i>",
        reply_markup=type_content.as_markup(),
        parse_mode="HTML"
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
    faq_text = (
        "<b>Зачем нужен этот бот?</b>\n"
        "<i>Чтобы ты не пропускал новый контент! "
        "Бот присылает уведомления о новых битах, стримах и конкурсах.</i>\n\n"

        "<b>Бот будет спамить?</b>\n"
        "<i>Нет! Ты сам выбираешь на что подписываться. Получишь только то, что выбрал.</i>\n\n"

        "<b>Как подписаться на рассылку?</b>\n"
        "<i>Зайди в</i> 📢 РАССЫЛКА → <i>выбери нужную категорию</i> → <i>готово!</i>"
    )

    await message.answer(faq_text, parse_mode="HTML")


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