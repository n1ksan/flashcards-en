import os
import time
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

BOT_TOKEN  = os.environ["BOT_TOKEN"]
WEBAPP_URL = os.environ["WEBAPP_URL"]
APP_VERSION = str(int(time.time()))

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sep = '&' if '?' in WEBAPP_URL else '?'
    url = f"{WEBAPP_URL}{sep}v={APP_VERSION}"
    keyboard = [
        [InlineKeyboardButton("✦ Открыть Flashcards", web_app=WebAppInfo(url=url))],
    ]
    await update.message.reply_text(
        "👋 Привет!\n\nВыбери нужные наборы и начни изучение:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    logging.info("Bot started. Polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
