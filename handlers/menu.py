from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

router = Router()

@router.message(Command(commands=["start", "menu"]))
async def show_menu(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📊 Портфель"))
    kb.add(KeyboardButton("➕ Добавить актив"))
    await message.reply("📍 Главное меню", reply_markup=kb)

@router.message(F.text == "📊 Портфель")
async def handle_portfolio_button(message: types.Message):
    await message.answer("/list")  # Просто триггерим команду

@router.message(F.text == "➕ Добавить актив")
async def handle_add_button(message: types.Message):
    await message.reply("✏️ Введи команду: /add BTC 0.5")
