from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def show_main_menu(message: Message):
    logger.info(f"📥 Получен /start от {message.from_user.id}")

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Портфель")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )

    await message.answer("📍 Главное меню", reply_markup=kb)
