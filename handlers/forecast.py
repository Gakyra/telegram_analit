# handlers/forecast.py
from aiogram import Router
from aiogram.types import Message
from app.services.forecast_service import get_latest_forecasts

router = Router()

@router.message(lambda msg: msg.text.lower() == "прогнозы")
async def handle_forecasts(message: Message):
    forecasts = get_latest_forecasts()
    if not forecasts:
        await message.answer("Нет доступных прогнозов.")
    else:
        text = "\n\n".join([
            f"🔮 {f.asset_name}\nДата: {f.created_at.strftime('%d.%m.%Y')}\nПрогноз: {f.prediction}"
            for f in forecasts
        ])
        await message.answer(f"Последние прогнозы:\n{text}")
