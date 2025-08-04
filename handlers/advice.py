# handlers/advice.py
from aiogram import Router
from aiogram.types import Message
from app.services.advice_service import get_psychology_advice
from app.models import User
from flask import current_app

router = Router()

@router.message(lambda msg: msg.text.lower() == "совет")
async def handle_advice(message: Message):
    user_id = message.from_user.id
    with current_app.app_context():
        user = User.query.filter_by(tg_id=user_id).first()
        if not user:
            await message.answer("Сначала зарегистрируйся через /start.")
        else:
            advice = get_psychology_advice(user)
            await message.answer(f"🧠 Совет: {advice}")
