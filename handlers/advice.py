from aiogram import Router, types
import random

router = Router()

TIPS = [
    "🧘 Дыши глубоко. Паника мешает видеть рынок.",
    "💡 Лучше держать, чем убегать в минус.",
    "⚖️ Не инвестируй эмоционально. Думай как аналитик.",
    "🎯 Стратегия важнее тренда. Не прыгай вслепую."
]

@router.message(lambda msg: msg.text == "/advice")
async def advice_handler(message: types.Message):
    tip = random.choice(TIPS)
    await message.answer(f"🧠 Психологический совет:\n{tip}")
