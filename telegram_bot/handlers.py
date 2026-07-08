import asyncio

from openai import RateLimitError
from telegram import Update
from telegram.ext import ContextTypes

from app.config import TELEGRAM_HELP_MESSAGE, TELEGRAM_WELCOME_MESSAGE
from app.logger import get_logger
from graph.workflow import workflow
from telegram_bot.constants import USER_DATA_FORMATTED_CONTENT, USER_DATA_WORKFLOW_INPUT
from telegram_bot.keyboards import preview_keyboard

logger = get_logger(__name__)


async def run_workflow_for_topic(topic: str, iteration: int = 0):
    workflow_input = {"topic": topic, "iteration": iteration}
    return await asyncio.to_thread(workflow.invoke, workflow_input)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    print(update.effective_chat.id)

    await update.message.reply_html(
        TELEGRAM_WELCOME_MESSAGE.format(user=user.mention_html())
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(TELEGRAM_HELP_MESSAGE)


async def generate_content(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if message is None:
        return

    topic = " ".join(context.args).strip() if context.args else message.text.strip()
    if topic.startswith("/write"):
        topic = topic.replace("/write", "", 1).strip()

    if not topic:
        await message.reply_text("Send a topic after /write to generate a poem.")
        return

    status_message = await message.reply_text(
        "⏳ Please wait while we generate your content..."
    )

    try:
        result = await run_workflow_for_topic(topic, iteration=0)
        formatted_content = result["formatted_content"]

    except RateLimitError:
        await status_message.delete()

        await message.reply_text(
            "⚠️ Daily AI generation limit reached.\n\n"
            "Please try again later."
        )
        return

    except Exception as exc:
        await status_message.delete()

        logger.exception("Content generation failed")
        await message.reply_text(
            "❌ Failed to generate content."
        )
        return

    context.user_data[USER_DATA_WORKFLOW_INPUT] = {
        "topic": topic,
        "iteration": 0,
    }
    context.user_data[USER_DATA_FORMATTED_CONTENT] = formatted_content

    await status_message.delete()

    await message.reply_html(
        formatted_content,
        reply_markup=preview_keyboard,
    )