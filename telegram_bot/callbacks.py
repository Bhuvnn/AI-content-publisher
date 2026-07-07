from telegram import Update
from telegram.ext import ContextTypes

from app.logger import get_logger
from telegram_bot.constants import (
    CALLBACK_CANCEL,
    CALLBACK_PUBLISH,
    CALLBACK_REGENERATE,
    USER_DATA_FORMATTED_CONTENT,
    USER_DATA_WORKFLOW_INPUT,
)
from telegram_bot.handlers import run_workflow_for_topic
from telegram_bot.keyboards import build_preview_keyboard
from telegram_bot.publisher import publish_to_channel

logger = get_logger(__name__)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None:
        return

    await query.answer()

    action = query.data
    message = query.message
    if message is None:
        return

    if action == CALLBACK_PUBLISH:
        formatted_content = context.user_data.get(USER_DATA_FORMATTED_CONTENT)
        if not formatted_content:
            await message.edit_text("This preview is no longer available.", reply_markup=None)
            return

        try:
            await publish_to_channel(context.bot, formatted_content)
        except Exception as exc:
            logger.exception("Failed to publish formatted content")
            await message.edit_text(f"Publishing failed: {exc}", reply_markup=None)
            return

        await message.edit_text(
            f"✅ Published to the Telegram channel.\n\n{formatted_content}",
            parse_mode="HTML",
            reply_markup=None,
        )
        return

    if action == CALLBACK_REGENERATE:
        workflow_input = context.user_data.get(USER_DATA_WORKFLOW_INPUT)
        if not workflow_input or "topic" not in workflow_input:
            await message.edit_text("This preview is no longer available.", reply_markup=None)
            return

        try:
            result = await run_workflow_for_topic(
                workflow_input["topic"],
                iteration=workflow_input.get("iteration", 0),
            )
            formatted_content = result["formatted_content"]
        except Exception as exc:
            logger.exception("Failed to regenerate formatted content")
            await message.edit_text(f"Regeneration failed: {exc}", reply_markup=None)
            return

        context.user_data[USER_DATA_FORMATTED_CONTENT] = formatted_content
        context.user_data[USER_DATA_WORKFLOW_INPUT] = {
            "topic": workflow_input["topic"],
            "iteration": workflow_input.get("iteration", 0),
        }

        await message.edit_text(
            formatted_content,
            parse_mode="HTML",
            reply_markup=build_preview_keyboard(),
        )
        return

    if action == CALLBACK_CANCEL:
        await message.edit_text("❌ Publication canceled.", reply_markup=None)
        return

    logger.warning("Unknown callback action received: %s", action)
    await message.edit_text("This action is not available anymore.", reply_markup=None)