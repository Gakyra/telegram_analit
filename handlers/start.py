from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
import logging

router = Router()
logger = logging.getLogger(__name__)

# ✅ Главное меню
async def send_main_menu(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Мой профиль")],
            [KeyboardButton(text="🧠 Психология")],
            [KeyboardButton(text="📈 Котировки")],
            [KeyboardButton(text="📊 Прогноз")],
            [KeyboardButton(text="📰 Новости"), KeyboardButton(text="🔔 Напомнить о важных событиях")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    await message.answer("📍 Главное меню", reply_markup=kb)


# ✅ Команда /start
@router.message(CommandStart())
async def show_main_menu_on_start(message: Message, state: FSMContext):
    logger.info(f"📥 Получен /start от {message.from_user.id}")
    await state.clear()
    await send_main_menu(message)

# ✅ Назад
@router.message(F.text == "🔙 Назад")
async def go_back(message: Message, state: FSMContext):
    await state.clear()
    await send_main_menu(message)
