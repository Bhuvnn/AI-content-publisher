from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler
from app.scheduler import start_scheduler
from telegram_bot.callbacks import handle_callback
from app.config import BOT_TOKEN, TELEGRAM_WELCOME_MESSAGE
from telegram_bot.handlers import generate_content, help_command, start

async def post_init(application: Application):
    start_scheduler(application)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()


    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("write", generate_content))
    application.add_handler(CallbackQueryHandler(handle_callback))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()