from telegram import Update
from telegram.ext import ContextTypes

from app.logger import get_logger
from telegram_bot.constants import (
    CALLBACK_CANCEL,
    CALLBACK_PUBLISH,
    CALLBACK_REGENERATE,
    USER_DATA_FORMATTED_CONTENT,
    USER_DATA_WORKFLOW_INPUT,
    WORKFLOW_CONTENT,
)
from telegram_bot.handlers import run_workflow_for_topic
from telegram_bot.keyboards import build_preview_keyboard
from telegram_bot.publisher import publish_to_channel
from database.crud import save_poem

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
        workflow = context.user_data.get(WORKFLOW_CONTENT)
        if not workflow or "formatted_content" not in workflow:
            await message.edit_text("This preview is no longer available.", reply_markup=None)
            return

        try:
            sent_message = await publish_to_channel(context.bot, workflow["formatted_content"])
            save_poem(workflow, sent_message.message_id)
        except Exception as exc:
            logger.exception("Failed to publish formatted content")
            await message.edit_text(f"Publishing failed: {exc}", reply_markup=None)
            return

        await message.edit_text(
            f"✅ Published to the Telegram channel.\n\n{workflow['formatted_content']}",
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

        context.user_data[WORKFLOW_CONTENT] = result
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