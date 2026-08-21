import os
import asyncio
import logging
from telethon import TelegramClient, events

# === Настройки из переменных окружения ===
API_ID = int(os.getenv("API_ID"))          # из my.telegram.org
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")         # ваш бот-токен (для отправки уведомлений)
OWNER_ID = int(os.getenv("OWNER_ID"))      # ваш Telegram ID

# Если нет бота – можно отправлять уведомления с самого клиента
# Но для удобства используем бота для рассылки

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаём клиент
client = TelegramClient("session", API_ID, API_HASH)

# Функция отправки уведомления через бота
async def notify_owner(text):
    from telegram import Bot
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=OWNER_ID, text=text, parse_mode="Markdown")

# Обработчик новых сообщений
@client.on(events.NewMessage)
async def handler(event):
    # Проверяем, что это сообщение из канала (или из группы)
    # event.chat – может быть каналом, группой, пользователем
    # Фильтруем только каналы (если нужно только каналы)
    # if not event.is_channel:
    #     return

    text = event.message.text or event.message.caption or ""
    if "роутер" in text.lower():
        chat = await event.get_chat()
        user = await event.get_sender()
        msg = (
            f"🔍 *Найдено 'роутер' в:*\n"
            f"Канал/чат: {chat.title or 'Приват'}\n"
            f"От: {user.first_name or user.username or 'Неизвестно'}\n"
            f"Текст: {text[:200]}..."
        )
        try:
            await notify_owner(msg)
        except Exception as e:
            logger.error(f"Не удалось отправить уведомление: {e}")

async def main():
    logger.info("Запуск клиента...")
    await client.start()
    logger.info("Клиент запущен, слушаем все сообщения из каналов и групп.")
    # Бесконечный цикл (пока не остановим)
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
