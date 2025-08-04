# handlers/profile.py
from aiogram import Router
from aiogram.types import Message
from flask import current_app
from app.models import User

router = Router()

@router.message(lambda msg: msg.text.lower() == "профиль")
async def handle_profile(message: Message):
    user_id = message.from_user.id
    with current_app.app_context():
        user = User.query.filter_by(tg_id=user_id).first()
        if not user:
            await message.answer("Профиль не найден. Используй /start для регистрации.")
        else:
            await message.answer(
                f"👤 Имя: {user.name}\nРиск: {user.risk_profile}\nПочта: {user.email}"
            )
