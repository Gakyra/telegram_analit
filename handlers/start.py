from aiogram import Router, types
from keyboards.menu import menu_keyboard

router = Router()

@router.message(lambda msg: msg.text == "/start")
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать! Я покажу ваш портфель, советы, прогнозы и профиль.",
        reply_markup=menu_keyboard
    )
