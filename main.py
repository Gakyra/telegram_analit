import asyncio
from aiogram import Bot, Dispatcher
from utils.config import TELEGRAM_TOKEN
from handlers import start, portfolio, advice, forecast, profile


from app import create_app
flask_app = create_app()

bot = Bot(token=TELEGRAM_TOKEN)
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
