from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .constants import CALLBACK_CANCEL, CALLBACK_PUBLISH, CALLBACK_REGENERATE


def build_preview_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ Publish", callback_data=CALLBACK_PUBLISH),
                InlineKeyboardButton("🔄 Regenerate", callback_data=CALLBACK_REGENERATE),
            ],
            [InlineKeyboardButton("❌ Cancel", callback_data=CALLBACK_CANCEL)],
        ]
    )


preview_keyboard = build_preview_keyboard()