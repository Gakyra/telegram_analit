from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/portfolio")],
        [KeyboardButton(text="/advice")],
        [KeyboardButton(text="/forecast")],
        [KeyboardButton(text="/profile")],
    ],
    resize_keyboard=True
)
