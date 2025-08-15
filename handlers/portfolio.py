from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from services.assets import get_available_assets, get_asset_price
from database import add_to_portfolio, get_user_portfolio

router = Router()

class AddAssetFSM(StatesGroup):
    choosing_asset = State()
    entering_amount = State()

@router.message(F.text == "📊 Портфель")
async def show_portfolio_menu(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Добавить актив")],
            [KeyboardButton(text="📈 Мой портфель")]
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите действие:", reply_markup=kb)

@router.message(F.text == "➕ Добавить актив")
async def start_add_asset(message: types.Message, state: FSMContext):
    assets = get_available_assets()
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=asset)] for asset in assets],
        resize_keyboard=True
    )
    await message.answer("Выбери актив для добавления:", reply_markup=kb)
    await state.set_state(AddAssetFSM.choosing_asset)

@router.message(AddAssetFSM.choosing_asset)
async def choose_asset(message: types.Message, state: FSMContext):
    await state.update_data(asset=message.text)
    await message.answer("✏️ Введи количество:")
    await state.set_state(AddAssetFSM.entering_amount)

@router.message(AddAssetFSM.entering_amount)
async def enter_amount(message: types.Message, state: FSMContext):
    data = await state.get_data()
    asset = data["asset"]
    try:
        amount = float(message.text)
    except ValueError:
        await message.answer("❌ Введи число.")
        return

    price = get_asset_price(asset)
    total_value = round(price * amount, 2)
    add_to_portfolio(user_id=message.from_user.id, asset=asset, amount=amount, price=price)

    await message.answer(f"✅ Добавлено: {asset} × {amount} по цене ${price} = ${total_value}")
    await state.clear()

@router.message(F.text == "📈 Мой портфель")
async def show_portfolio(message: types.Message):
    portfolio = get_user_portfolio(message.from_user.id)
    if not portfolio:
        await message.answer("📭 Портфель пуст")
        return

    lines = []
    for item in portfolio:
        current_price = get_asset_price(item["asset"])
        value = round(current_price * item["amount"], 2)
        lines.append(f"{item['asset']}: {item['amount']} × ${current_price} = ${value}")

    await message.answer("\n".join(lines))