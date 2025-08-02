import asyncio
from aiogram import Bot, Dispatcher
from handlers import start, portfolio, advice, forecast, profile

# 🔐 Загрузка .env до всего остального
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# 📊 Лог окружения
print(f"[LOG] TELEGRAM_TOKEN = {os.getenv('TELEGRAM_TOKEN')}")
print(f"[LOG] DATABASE_URL = {os.getenv('DATABASE_URL')}")

# 👇 Flask-приложение подключается после загрузки окружения
from app import create_app
from flask_analit.extensions import db

# 📦 Инициализация Flask-приложения
flask_app = create_app()

# 🔁 Импорт моделей внутри app_context — безопасно!
with flask_app.app_context():
    import flask_analit.models  # просто импортируем весь модуль
    db.create_all()

# 🤖 Telegram-бот
bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(portfolio.router)
dp.include_router(advice.router)
dp.include_router(forecast.router)
dp.include_router(profile.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
