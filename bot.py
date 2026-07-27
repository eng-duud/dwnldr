from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers import start_command, help_command, info_command, video_command, audio_command, message_handler, post_init, shutdown
from logger import logger
from telegram import Update

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found in .env file. Please set it.")
        return

    application = Application.builder().token(BOT_TOKEN).post_init(post_init).post_shutdown(shutdown).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("video", video_command))
    application.add_handler(CommandHandler("audio", audio_command))

    # Message Handler for URLs and other text
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    logger.info("Bot started polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
