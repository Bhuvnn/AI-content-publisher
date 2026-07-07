from telegram import Bot

from app.config import TELEGRAM_CHANNEL_ID
from app.logger import get_logger

logger = get_logger(__name__)


async def publish_to_channel(bot: Bot, formatted_content: str):
    if not TELEGRAM_CHANNEL_ID:
        raise ValueError("TELEGRAM_CHANNEL_ID is not configured.")

    logger.info("Publishing formatted content to Telegram channel %s", TELEGRAM_CHANNEL_ID)
    return await bot.send_message(
        chat_id=TELEGRAM_CHANNEL_ID,
        text=formatted_content,
        parse_mode="HTML",
    )