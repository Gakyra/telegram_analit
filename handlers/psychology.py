from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import random

router = Router()

# FSM состояния
class PsychologyState(StatesGroup):
    waiting_for_topic = State()
    showing_tip = State()

# Темы и советы
TIPS = {
    "📌 Эмоции": [
        "😤 Эмоции — главный враг трейдера. Учись распознавать импульсивные решения.",
        "😱 Паника на рынке — сигнал для анализа, не для действий.",
        "😌 Умение сохранять спокойствие — ключ к долгосрочному успеху.",
        "🧠 Страх и жадность искажают восприятие. Доверяй стратегии, не ощущениям.",
        "😮‍💨 Не реагируй на каждое движение рынка — это путь к выгоранию.",
        "😵‍💫 Эмоциональные качели мешают объективности. Пиши план и следуй ему."
    ],
    "📈 Дисциплина": [
        "📊 Следуй стратегии, а не шуму. Новости — не всегда сигнал.",
        "🧘 Дисциплина важнее прогноза. Умей ждать и не паниковать.",
        "🛑 Не усредняй убытки без плана. Это ловушка для эмоций.",
        "📋 Веди журнал сделок — это зеркало твоей дисциплины.",
        "📌 Дисциплина — это привычка, а не вдохновение."
    ],
    "🧘 Мышление инвестора": [
        "🧠 Мышление инвестора — это терпение, анализ и адаптация.",
        "📉 Потери — часть игры. Главное — учиться и адаптироваться.",
        "🧘 Умей выйти из позиции. Фиксация прибыли — тоже стратегия.",
        "🧩 Не ищи идеальную точку входа — ищи хорошую идею и реализацию.",
        "🧭 Не гонись за трендами — строй свою карту."
    ],
    "🎯 Цели": [
        "🎯 Ставь цели: доходность, срок, риск — и проверяй их регулярно.",
        "📅 Планируй: когда входить, когда выходить, когда пересматривать портфель.",
        "📌 Без цели — нет стратегии. Без стратегии — только хаос.",
        "📈 Цели помогают фильтровать шум и фокусироваться на сути.",
        "🧭 Цель — это компас, а не якорь."
    ]
}

# Меню психологии
@router.message(F.text == "🧠 Психология")
async def show_psychology_menu(message: Message, state: FSMContext):
    await state.set_state(PsychologyState.waiting_for_topic)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📌 Эмоции"), KeyboardButton(text="📈 Дисциплина")],
            [KeyboardButton(text="🧘 Мышление инвестора"), KeyboardButton(text="🎯 Цели")],
            [KeyboardButton(text="📚 Рекомендации")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите тему"
    )
    await message.answer("🧠 Психология инвестора\nВыберите тему:", reply_markup=kb)

# Выбор темы → совет
@router.message(PsychologyState.waiting_for_topic, F.text.in_(TIPS.keys()))
async def show_tip(message: Message, state: FSMContext):
    topic = message.text
    await state.update_data(topic=topic)
    await state.set_state(PsychologyState.showing_tip)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Ещё")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    tip = random.choice(TIPS[topic])
    await message.answer(tip, reply_markup=kb)

# Ещё совет
@router.message(PsychologyState.showing_tip, F.text == "Ещё")
async def show_another_tip(message: Message, state: FSMContext):
    data = await state.get_data()
    topic = data.get("topic")
    tip = random.choice(TIPS[topic])
    await message.answer(tip)

# Рекомендации
@router.message(F.text == "📚 Рекомендации")
async def show_recommendations(message: Message):
    text = (
        "📚 *Рекомендации по психологии инвестиций:*\n\n"
        "🔸 _Книги:_\n"
        "• «Психология инвестирования» — Джон Нофсингер\n"
        "• «Думай медленно… решай быстро» — Даниэль Канеман\n"
        "• «Поведенческие финансы» — Джеймс Монтиер\n\n"
        "🔸 _YouTube:_\n"
        "• Rational Reminder\n"
        "• Aswath Damodaran\n"
        "• Investopedia\n\n"
        "🔸 _Статьи:_\n"
        "• «Why Investors Behave Irrationally» — CFA Institute\n"
        "• «The Psychology of Market Cycles» — Morningstar\n\n"
        "💡 Эти ресурсы помогут прокачать мышление, дисциплину и устойчивость к шуму."
    )
    await message.answer(text, parse_mode="Markdown")

# Назад
@router.message(F.text == "🔙 Назад")
async def go_back(message: Message, state: FSMContext):
    await state.clear()
    from handlers.start import send_main_menu
    await send_main_menu(message)
