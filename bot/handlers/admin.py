import logging
from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.database import Database


class BroadcastForm(StatesGroup):
    category = State()
    message = State()


async def start_broadcast(message: types.Message, state: FSMContext, db: Database):
    if not db.is_admin(message.from_user.id):
        return
    await state.set_state(BroadcastForm.category)
    await message.answer(
        "Выбери категорию для рассылки (beats, music_streams, music_only, games, all):"
    )


async def get_category(message: types.Message, state: FSMContext):
    category = message.text.strip().lower()
    valid_categories = {"beats", "music_streams", "music_only", "games", "all"}
    if category not in valid_categories:
        await message.answer("Ошибка в названии категории")
        return
    await state.update_data(category=category)
    await state.set_state(BroadcastForm.message)
    await message.answer("Введи сообщение для рассылки")


async def send_broadcast(message: types.Message, state: FSMContext, bot: Bot, db: Database):
    data = await state.get_data()
    category = data['category']
    subscribers = db.get_subscribers_by_category(category)
    if not subscribers:
        await message.answer("Нет подписчиков в этой категории!")
        await state.clear()
        return

    sent_count = 0
    for user_id in subscribers:
        try:
            await bot.copy_message(
                chat_id=user_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            sent_count += 1
        except Exception as e:
            logging.error(f"Ошибка отправки {user_id}: {e}")
    await message.answer(f"Рассылка отправлена {sent_count} пользователям!")
    await state.clear()