import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.start import router as start_router
from handlers.portfolio import router as portfolio_router
from handlers.psychology import router as psychology_router
from db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ TELEGRAM_TOKEN не найден. Проверь .env файл и переменную.")

async def main():
    logger.info("🚀 Запуск бота...")
    await init_db()

    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("🔧 Webhook удалён (если был)")

    dp.include_router(start_router)
    dp.include_router(portfolio_router)
    dp.include_router(psychology_router)
    logger.info("✅ Роутеры подключены")

    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота")
    ])
    logger.info("✅ Команды установлены")

    logger.info("📡 Ожидание обновлений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
