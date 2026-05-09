import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

BOT_TOKEN  = os.environ["BOT_TOKEN"]
WEBAPP_URL = os.environ["WEBAPP_URL"]

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("📚 Тематический набор (164 слова)", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("🎓 B2 словарь (500 слов)", web_app=WebAppInfo(url=WEBAPP_URL.rstrip("/") + "/b2/"))],
    ]
    await update.message.reply_text(
        "👋 Привет!\n\nВыбери набор для изучения:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    logging.info("Bot started. Polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
