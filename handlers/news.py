from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.inline import news_filters_kb
from services.calendar import get_events_by_date, get_upcoming_important_events, KYIV_TZ
from datetime import datetime
router = Router()

class NewsState(StatesGroup):
    choosing_period = State()

@router.message(F.text == "📰 Новости")
async def news_entry(message: types.Message, state: FSMContext):
    await message.answer("Выбери период:", reply_markup=news_filters_kb.period())
    await state.set_state(NewsState.choosing_period)

@router.callback_query(NewsState.choosing_period)
async def period_chosen(callback: types.CallbackQuery, state: FSMContext):
    mode = callback.data  # "today", "tomorrow", "week"
    events = await get_events_by_date(mode)

    if not events or events[0]["event"].startswith("События на выбранную дату отсутствуют"):
        await callback.message.edit_text("Нет событий на выбранную дату.")
        return

    text = f"📰 События ({mode}):\n\n"
    for e in events[:10]:
        dt = e.get("datetime")
        now = datetime.now(KYIV_TZ)
        status = "🕒 Ожидается"
        if dt and dt < now:
            status = "✅ Уже прошло"
        if e["actual"] != "-":
            status = "📊 Опубликовано"

        text += (
            f"• {e['time']} — {e['event']}\n"
            f"  Статус: {status}\n"
            f"  Факт: {e['actual']} | Прогноз: {e['forecast']} | Пред: {e['previous']}\n\n"
        )

    await callback.message.edit_text(text.strip())

@router.message(F.text == "🔔 Напомнить о важных событиях")
async def remind_important(message: types.Message):
    upcoming = await get_upcoming_important_events()

    if not upcoming:
        await message.answer("Сегодня больше нет важных событий.")
        return

    text = "🔔 Ближайшие важные события:\n\n"
    for e in upcoming[:5]:
        text += f"• {e['time']} — {e['event']}\n"

    await message.answer(text.strip())
