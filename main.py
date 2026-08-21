import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set!")
if OWNER_ID == 0:
    logging.warning("OWNER_ID not set, notifications will not work.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Название группы, которую нужно отслеживать (можно указать точное название)
TARGET_GROUP_NAME = "InnoAds"   # Если название на русском – пишите как в Telegram

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_message:
        return

    chat = update.effective_chat

    text = update.effective_message.text or update.effective_message.caption or ""
    if "роутер" in text.lower():
        user = update.effective_user
        msg = (
            f"🔍 *Найдено 'роутер' в группе {chat.title}:*\n"
            f"От: @{user.username or user.full_name}\n"
            f"Текст: {text[:200]}..."
        )
        try:
            await context.bot.send_message(chat_id=OWNER_ID, text=msg, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Не удалось отправить уведомление: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, message_handler))
    logger.info("Бот запущен, отслеживаю группу InnoAds...")
    app.run_polling()

if __name__ == "__main__":
    main()
