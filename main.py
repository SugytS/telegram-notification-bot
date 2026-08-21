import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- Configuration ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))  # your Telegram user ID
WEBHOOK_URL = os.getenv("WEBHOOK_URL")     # public URL of your web service

if not BOT_TOKEN or not OWNER_ID or not WEBHOOK_URL:
    raise ValueError("Missing environment variables: BOT_TOKEN, OWNER_ID, WEBHOOK_URL")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Message handler ---
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check each incoming message for the keyword."""
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

# --- Main app ---
def main():
    # Create Application
    app = Application.builder().token(BOT_TOKEN).build()

    # Add handler for all messages (including edited)
    app.add_handler(MessageHandler(filters.ALL, message_handler))

    # Set webhook (on startup)
    app.bot.set_webhook(url=WEBHOOK_URL)

    # Start webhook server
    logger.info(f"Starting webhook on {WEBHOOK_URL}")
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        webhook_url=WEBHOOK_URL,
    )

if __name__ == "__main__":
    main()
