import asyncio
import logging
import os
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNEL_ID = os.getenv('CHANNEL_ID')

if not YOUTUBE_API_KEY:
    raise ValueError("Не установлен YOUTUBE_API_KEY")
if not CHANNEL_ID:
    raise ValueError("Не установлен CHANNEL_ID")

logger = logging.getLogger(__name__)


async def monitor_youtube(bot, db):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    last_video_id = None

    while True:
        try:
            response = youtube.search().list(
                part="id,snippet",
                channelId=CHANNEL_ID,
                type="video",
                order="date",
                maxResults=2
            ).execute()

            items = response.get("items", [])
            for item in reversed(items):  # от старого к новому, чтобы не пропустить
                video_id = item["id"]["videoId"]
                if video_id == last_video_id:
                    continue

                title = item["snippet"]["title"]
                url = f"https://youtu.be/{video_id}"
                message = f"Новый бит: {title}\n{url}"

                subscribers = db.get_subscribers_by_category("beats")
                for user_id in subscribers:
                    try:
                        await bot.send_message(user_id, message)
                    except Exception as send_err:
                        logger.error(f"Ошибка отправки {user_id}: {send_err}")

                last_video_id = video_id
                logger.info(f"Отправлено новое видео: {title}")

        except HttpError as api_err:
            logger.error(f"YouTube API ошибка: {api_err}")
            if api_err.resp.status in (403, 429):
                await asyncio.sleep(3600)
                continue
        except Exception as e:
            logger.exception("Неизвестная ошибка в мониторинге YouTube")

        await asyncio.sleep(600)  # проверка каждые 10 минут