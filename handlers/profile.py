from aiogram import Router, types
from flask_analit.models import User
from utils.database import app

router = Router()

@router.message(lambda msg: msg.text == "/profile")
async def profile_handler(message: types.Message):
    telegram_id = message.from_user.id
    with app.app_context():
        user = User.query.filter_by(telegram_id=telegram_id).first()
        if not user:
            await message.answer("🙅 Пользователь не найден.")
        else:
            role = "🛡️ Админ" if user.is_admin else "👤 Пользователь"
            await message.answer(
                f"👤 Профиль:\nИмя: {user.username}\nEmail: {user.email}\nСтатус: {role}"
            )
