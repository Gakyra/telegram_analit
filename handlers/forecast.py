from aiogram import Router, types
from flask_analit.models import Forecast
from utils.database import app

router = Router()

@router.message(lambda msg: msg.text == "/forecast")
async def forecast_handler(message: types.Message):
    telegram_id = message.from_user.id
    with app.app_context():
        user = Forecast.query.filter_by(user_id=telegram_id).order_by(Forecast.created_at.desc()).first()
        if not user:
            await message.answer("🔮 Нет доступных прогнозов.")
        else:
            await message.answer(f"📈 Последний прогноз по {user.symbol}:\n{user.predicted}")
