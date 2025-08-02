from aiogram import Router, types
from utils.database import get_user_portfolio

router = Router()

@router.message(lambda msg: msg.text == "/portfolio")
async def portfolio_handler(message: types.Message):
    telegram_id = message.from_user.id
    result = get_user_portfolio(telegram_id)
    await message.answer(f"📊 Ваш портфель:\n{result}")
