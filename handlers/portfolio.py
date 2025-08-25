from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import logging
import aiohttp
import asyncio
import random
from datetime import datetime, timedelta

from db import add_asset, get_portfolio, reset_portfolio
from handlers.start import send_main_menu

router = Router()
logger = logging.getLogger(__name__)

class PortfolioFSM(StatesGroup):
    choosing_asset = State()
    entering_amount = State()
    entering_buy_price = State()

ASSETS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "XRP": "ripple",
    "USDT": "tether",
    "BNB": "binancecoin"
}

VOLATILITY = {
    "BTC": 0.6,
    "ETH": 0.5,
    "XRP": 0.4,
    "USDT": 0.05,
    "BNB": 0.3
}

# ✅ Кэш цен: { 'BTC': (116435.0, datetime) }
price_cache = {}

async def get_prices(assets: list[str]) -> dict[str, float]:
    now = datetime.utcnow()
    result = {}
    to_fetch = []

    for asset in assets:
        cached = price_cache.get(asset)
        if cached and now - cached[1] < timedelta(minutes=5):
            result[asset] = cached[0]
        else:
            to_fetch.append(asset)

    ids = [ASSETS[a] for a in to_fetch if a in ASSETS]
    if not ids:
        return result

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(ids)}&vs_currencies=usd"
    headers = {"User-Agent": "Mozilla/5.0"}

    for attempt in range(3):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 429:
                        logger.warning("❌ Ошибка запроса CoinGecko: 429 — превышен лимит")
                        await asyncio.sleep(2 ** attempt)
                        continue
                    data = await resp.json()
                    for asset in to_fetch:
                        coin_id = ASSETS.get(asset)
                        if coin_id in data and "usd" in data[coin_id]:
                            price = data[coin_id]["usd"]
                            result[asset] = price
                            price_cache[asset] = (price, now)
            break
        except Exception as e:
            logger.error(f"❌ Ошибка запроса CoinGecko: {e}")
            break

    return result
@router.message(F.text == "📊 Мой профиль")
async def show_profile_menu(message: Message):
    portfolio = await get_portfolio(message.from_user.id)
    if not portfolio:
        await message.answer("📭 Ваш портфель пуст.")
    else:
        assets = list(set([row[0] for row in portfolio]))
        prices = await get_prices(assets)

        total_profit = 0
        text = "👤 Ваш портфель:\n"

        for asset, amount, buy_price in portfolio:
            current_price = prices.get(asset, 0)
            total_value = round(current_price * amount, 2)
            profit = round((current_price - buy_price) * amount, 2)
            total_profit += profit

            status = "📈 Прибыль" if profit > 0 else "📉 Убыток" if profit < 0 else "⚖️ Без изменений"
            warning = " ⚠️ Цена не получена" if current_price == 0 else ""
            text += (
                f"\n• {asset}\n"
                f"  Кол-во: {amount}\n"
                f"  Цена покупки: ${buy_price}\n"
                f"  Текущая цена: ${current_price}{warning}\n"
                f"  Сумма: ${total_value}\n"
                f"  {status}: ${profit}\n"
            )

        summary = (
            f"📊 Общий результат: "
            f"{'📈 Прибыль' if total_profit > 0 else '📉 Убыток' if total_profit < 0 else '⚖️ Без изменений'} "
            f"${round(total_profit, 2)}\n\n"
        )
        await message.answer(summary + text)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Добавить актив")],
            [KeyboardButton(text="🗑 Очистить портфель")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    await message.answer("👤 Ваш профиль", reply_markup=kb)
@router.message(F.text == "➕ Добавить актив")
async def start_portfolio_flow(message: Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="BTC"), KeyboardButton(text="ETH")],
            [KeyboardButton(text="XRP"), KeyboardButton(text="USDT")],
            [KeyboardButton(text="BNB"), KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите актив"
    )
    await message.answer("💼 Выберите актив для добавления:", reply_markup=kb)
    await state.set_state(PortfolioFSM.choosing_asset)

@router.message(PortfolioFSM.choosing_asset, F.text.in_(ASSETS.keys()))
async def asset_chosen(message: Message, state: FSMContext):
    asset = message.text
    await state.update_data(asset=asset)
    await message.answer(f"Введите количество {asset}:")
    await state.set_state(PortfolioFSM.entering_amount)

@router.message(PortfolioFSM.entering_amount, F.text.regexp(r"^\d+(\.\d+)?$"))
async def amount_entered(message: Message, state: FSMContext):
    amount = float(message.text)
    await state.update_data(amount=amount)

    data = await state.get_data()
    asset = data.get("asset")
    prices = await get_prices([asset])
    current_price = prices.get(asset, 0)

    await message.answer(
        f"💰 Текущая цена {asset}: ${current_price}\n"
        f"Введите цену покупки:"
    )
    await state.set_state(PortfolioFSM.entering_buy_price)

@router.message(PortfolioFSM.entering_buy_price, F.text.regexp(r"^\d+(\.\d+)?$"))
async def buy_price_entered(message: Message, state: FSMContext):
    buy_price = float(message.text)
    data = await state.get_data()
    asset = data.get("asset")
    amount = data.get("amount")

    await add_asset(message.from_user.id, asset, amount, buy_price)
    await message.answer(f"✅ Добавлено: {amount} {asset} по цене ${buy_price}")
    await state.clear()
    await show_profile_menu(message)
@router.message(F.text == "🗑 Очистить портфель")
async def clear_portfolio(message: Message):
    await reset_portfolio(message.from_user.id)
    await message.answer("🧹 Портфель очищен.")
    await show_profile_menu(message)

@router.message(F.text == "📈 Котировки")
async def show_quotes(message: Message):
    assets = list(ASSETS.keys())
    prices = await get_prices(assets)

    text = "📈 Актуальные котировки:\n"
    for asset in assets:
        price = prices.get(asset, 0)
        warning = " ❌" if price == 0 else ""
        text += f"• {asset}: ${price}{warning}\n"

    await message.answer(text)
    await send_main_menu(message)

@router.message(F.text == "📊 Прогноз")
async def forecast_menu(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="BTC"), KeyboardButton(text="ETH")],
            [KeyboardButton(text="XRP"), KeyboardButton(text="USDT")],
            [KeyboardButton(text="BNB"), KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите актив для прогноза"
    )
    await message.answer("📈 Выберите актив для прогноза:", reply_markup=kb)

@router.message(F.text.in_(ASSETS.keys()))
async def show_forecast(message: Message):
    asset = message.text
    prices = await get_prices([asset])
    base_price = prices.get(asset, 0)
    if base_price == 0:
        await message.answer("❌ Не удалось получить цену. Попробуйте позже.")
        return

    volatility = VOLATILITY.get(asset, 0.3)
    forecast = [round(base_price, 2)]
    for _ in range(9):
        change_percent = random.gauss(mu=0.15, sigma=volatility)
        new_price = forecast[-1] * (1 + change_percent / 100)
        forecast.append(round(new_price, 2))

    text = f"📊 Прогноз цены {asset} на 10 дней:\n\n"
    for i, price in enumerate(forecast):
        if i == 0:
            text += f"День {i+1}\t${price}\n"
        else:
            prev = forecast[i - 1]
            delta = price - prev
            percent = round((delta / prev) * 100, 2)
            sign = "+" if percent > 0 else ""
            text += f"День {i+1}\t${price} ({sign}{percent}%)\n"

    await message.answer(text)
    await send_main_menu(message)
@router.message(F.text == "🔙 Назад")
async def go_back(message: Message, state: FSMContext):
    await state.clear()
    await send_main_menu(message)
