from aiogram import Router
from aiogram.types import Message
from app.services.portfolio_service import get_user_portfolio

router = Router()

@router.message(lambda msg: msg.text.lower() == "портфель")
async def handle_portfolio(message: Message):
    user_id = message.from_user.id
    portfolio = get_user_portfolio(user_id)
    if not portfolio:
        await message.answer("Портфель пуст.")
    else:
        text = "\n".join([f"{p.asset_name}: {p.amount}" for p in portfolio])
        await message.answer(f"Ваш портфель:\n{text}")
