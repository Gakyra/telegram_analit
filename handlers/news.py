from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.inline import news_filters_kb
from services.calendar import get_events_safe

from datetime import datetime

router = Router()

class NewsState(StatesGroup):
    choosing_country = State()
    choosing_importance = State()

# 📰 Вход в новости
@router.message(F.text == "📰 Новости")
async def news_entry(message: types.Message, state: FSMContext):
    await message.answer("Выбери страну:", reply_markup=news_filters_kb.country())
    await state.set_state(NewsState.choosing_country)

# 🌍 Выбор страны
@router.callback_query(NewsState.choosing_country)
async def country_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(country=callback.data)
    await callback.message.edit_text("Выбери важность событий:", reply_markup=news_filters_kb.importance())
    await state.set_state(NewsState.choosing_importance)

# 🔍 Выбор важности
@router.callback_query(NewsState.choosing_importance)
async def importance_chosen(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    country = data["country"]
    importance = int(callback.data)

    events = await get_events_safe(country_filter=[country], min_importance=importance)
    if not events or events[0]["event"] == "События временно недоступны":
        await callback.message.edit_text("Нет событий по выбранным фильтрам.")
        return

    text = f"📰 События ({country}, важность: {importance}):\n\n"
    for e in events[:10]:
        text += (
            f"• {e['time']} — {e['event']}\n"
            f"  Факт: {e['actual']} | Прогноз: {e['forecast']} | Пред: {e['previous']}\n\n"
        )

    await callback.message.edit_text(text.strip())

# 🔔 Напоминание о ближайших событиях
@router.message(F.text == "🔔 Напомнить о важных событиях")
async def remind_important(message: types.Message):
    events = await get_events_safe(country_filter=["United States"], min_importance=3)
    now = datetime.now().strftime("%H:%M")

    upcoming = [e for e in events if e["time"] >= now]
    if not upcoming:
        await message.answer("Сегодня больше нет важных событий.")
        return

    text = "🔔 Ближайшие важные события:\n\n"
    for e in upcoming[:5]:
        text += f"• {e['time']} — {e['event']}\n"

    await message.answer(text.strip())
