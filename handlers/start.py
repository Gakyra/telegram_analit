# handlers/start.py
from aiogram import Router
from aiogram.types import Message
from flask import current_app
from app.models import User
from app.services.advice_service import get_psychology_advice

router = Router()

@router.message(lambda msg: msg.text.lower() == "/start")
async def handle_start(message: Message):
    user_id = message.from_user.id
    with current_app.app_context():
        user = User.query.filter_by(tg_id=user_id).first()
        if not user:
            user = User(tg_id=user_id, name=message.from_user.full_name, risk_profile="balanced")
            current_app.extensions['sqlalchemy'].db.session.add(user)
            current_app.extensions['sqlalchemy'].db.session.commit()
            await message.answer(f"👋 Привет, {user.name}! Ты зарегистрирован.\nТвой риск-профиль: balanced")
        else:
            await message.answer(f"👋 С возвращением, {user.name}!\nТвой риск-профиль: {user.risk_profile}")
