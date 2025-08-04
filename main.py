import asyncio
from aiogram import Bot, Dispatcher
from handlers import start, portfolio, advice, forecast, profile

from dotenv import load_dotenv
from pathlib import Path
import os

# 🔐 Загрузка .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

print(f"[LOG] TELEGRAM_TOKEN = {os.getenv('TELEGRAM_TOKEN')}")
print(f"[LOG] DATABASE_URL = {os.getenv('DATABASE_URL')}")

from app import create_app
from flask_analit.extensions import db

# 📦 Создание и конфигурация Flask-приложения
flask_app = create_app()

# 🔁 Инициализация моделей и базы данных — строго внутри app_context
with flask_app.app_context():
    from flask_analit.models import (
        User, Asset, Post, Comment,
        Forecast, Investment, PortfolioHistory, log_history
    )
    db.create_all()

# 🤖 Telegram-бот
bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()

# 🔌 Подключение роутеров
dp.include_router(start.router)
dp.include_router(portfolio.router)
dp.include_router(advice.router)
dp.include_router(forecast.router)
dp.include_router(profile.router)

# 🚀 Запуск polling
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
