import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import start, portfolio

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def main():
    bot = Bot(token=TOKEN, parse_mode="HTML")  # ✅ parse_mode передаётся напрямую
    dp = Dispatcher(storage=MemoryStorage())

    # ✅ Подключаем роутеры
    dp.include_router(start.router)
    dp.include_router(portfolio.router)

    # ✅ Устанавливаем команды
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота")
    ])

    # ✅ Запускаем polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())