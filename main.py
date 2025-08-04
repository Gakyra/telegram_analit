import asyncio
from aiogram import Bot, Dispatcher
from handlers import start, portfolio, advice, forecast, profile

from dotenv import load_dotenv
from pathlib import Path
import os
from threading import Thread

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

from app import create_app
from flask_analit.extensions import db

flask_app = create_app()

with flask_app.app_context():
    from app.models import (
        User, Asset, Post, Comment,
        Forecast, Investment, PortfolioHistory, log_history
    )
    db.create_all()

def run_flask():
    flask_app.run(debug=False, use_reloader=False)

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(portfolio.router)
dp.include_router(advice.router)
dp.include_router(forecast.router)
dp.include_router(profile.router)

async def main():
    Thread(target=run_flask).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
