from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def show_main_menu(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Портфель")]
        ],
        resize_keyboard=True
    )
    await message.answer("📍 Главное меню", reply_markup=kb)