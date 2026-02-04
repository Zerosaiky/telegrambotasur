from aiogram import types
from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder, InlineKeyboardBuilder
)
from typing import Union, Tuple
from aiogram.types import InlineKeyboardMarkup


# можно просто оставить def get_subscription_list_keyboard(current=None), ничего не поменяется
def get_subscription_list_keyboard(current: Union[str, None] = None) -> Tuple[str, InlineKeyboardMarkup]:

    builder = InlineKeyboardBuilder()

    contents = [
        ("Биты",                    "sub_beats",         "beats"),
        ("Трансляции по музыке",    "sub_music_streams", "music_streams"),
        ("Только музыкальный контент", "sub_music_only", "music_only"),
        ("Игры",                    "sub_games",         "games"),
        ("Весь контент",            "sub_all",           "all"),
    ]

    for display_text, callback_data, db_value in contents:
        is_active = (current == db_value)
        status_emoji = "✅" if is_active else "❌"
        button_text = f"{status_emoji} {display_text}"
        builder.button(text=button_text, callback_data=callback_data)

    builder.adjust(1)

    status_line = f"Текущая подписка: <b>{current}</b>" if current else "Нет активной подписки"

    full_text = (
        "📢 <b>Управление подписками</b>\n\n"
        f"{status_line}\n\n"
        "✅ — Текущая подписка\n"
        "❌ — Можно подписаться\n\n"
        "<i>Нажми на кнопку, чтобы переключить</i>"
    )

    return full_text, builder.as_markup()


async def show_subscription_list(call_or_message, db, is_callback=False):
    user_id = call_or_message.from_user.id
    current = db.get_subscription(user_id)

    text, markup = get_subscription_list_keyboard(current)

    if is_callback:
        await call_or_message.message.edit_text(
            text,
            reply_markup=markup,
            parse_mode="HTML"
        )
    else:
        await call_or_message.answer(
            text,
            reply_markup=markup,
            parse_mode="HTML"
        )


async def show_subscription_success(call: types.CallbackQuery, db):
    user_id = call.from_user.id
    category = call.data[4:]

    new_status = db.toggle_subscription(user_id, category)

    if new_status:
        action = "подписался на"
        cat_display = new_status
    else:
        action = "отписался от"
        cat_display = category

    text = (
        f"Ты успешно <b>{action}</b> рассылки вида «{cat_display}» ✅\n\n"
        "Теперь бот будет присылать тебе уведомления "
        f"только об этом типе контента.\n\n"
        "<i>В любой момент можешь вернуться и поменять свой выбор</i>"
    )

    back_markup = InlineKeyboardBuilder()
    back_markup.button(text="← Назад к списку", callback_data="back_to_subs")

    await call.message.edit_text(
        text,
        reply_markup=back_markup.as_markup(),
        parse_mode="HTML"
    )


async def back_to_list(call: types.CallbackQuery, db):
    await show_subscription_list(call, db, is_callback=True)


async def newsletter(message: types.Message, db):
    await show_subscription_list(message, db, is_callback=False)


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