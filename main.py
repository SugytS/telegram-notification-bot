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

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_message:
        return
    text = update.effective_message.text or update.effective_message.caption or ""
    if "роутер" in text.lower():
        chat = update.effective_chat
        user = update.effective_user
        msg = (
            f"🔍 *Found 'роутер' in:*\n"
            f"Chat: {chat.title or chat.first_name or 'Private'}\n"
            f"User: @{user.username or user.full_name}\n"
            f"Message: {text[:200]}..."
        )
        try:
            await context.bot.send_message(chat_id=OWNER_ID, text=msg, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Failed to notify owner: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, message_handler))
    logger.info("Starting bot with long polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
