from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Портфель")],
        [KeyboardButton(text="Добавить актив")],
        [KeyboardButton(text="Настройки")]
    ],
    resize_keyboard=True
)

asset_selection_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="BTC"), KeyboardButton(text="ETH")],
        [KeyboardButton(text="SOL"), KeyboardButton(text="USDT")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True
)
