from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def country():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇸 США", callback_data="United States")],
        [InlineKeyboardButton(text="🇪🇺 Еврозона", callback_data="Euro Area")],
        [InlineKeyboardButton(text="🇯🇵 Япония", callback_data="Japan")],
        [InlineKeyboardButton(text="🇬🇧 Великобритания", callback_data="United Kingdom")]
    ])

def importance():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Важность 1", callback_data="1")],
        [InlineKeyboardButton(text="Важность 2", callback_data="2")],
        [InlineKeyboardButton(text="Важность 3", callback_data="3")]
    ])
