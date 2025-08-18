import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import start, portfolio

# ✅ Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ TELEGRAM_TOKEN не найден. Проверь .env файл и переменную.")

async def main():
    logger.info("🚀 Запуск бота...")
    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    # ✅ Удаляем webhook, если был
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("🔧 Webhook удалён (если был)")

    # ✅ Подключаем роутеры
    dp.include_router(start.router)
    dp.include_router(portfolio.router)
    logger.info("✅ Роутеры подключены: start, portfolio")

    # ✅ Устанавливаем команды
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота")
    ])
    logger.info("✅ Команды установлены")

    # ✅ Запускаем polling
    logger.info("📡 Ожидание обновлений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
