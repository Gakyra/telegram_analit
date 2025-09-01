from bs4 import BeautifulSoup
import aiohttp

cached_events = []

# 🌍 Маппинг ISO-кодов и названий на Telegram-названия
COUNTRY_MAP = {
    "US": "США",
    "UNITED STATES": "США",
    "EU": "Еврозона",
    "EUROZONE": "Еврозона",
    "JP": "Япония",
    "JAPAN": "Япония",
    "GB": "Великобритания",
    "UK": "Великобритания",
    "UNITED KINGDOM": "Великобритания"
}

def extract_country_name(row):
    # Пытаемся взять из data-country
    raw = row.get("data-country", "").strip().upper()
    if raw in COUNTRY_MAP:
        return COUNTRY_MAP[raw]

    # Пробуем title
    title = row.get("title", "").strip().upper()
    for key in COUNTRY_MAP:
        if key in title:
            return COUNTRY_MAP[key]

    # Пробуем aria-label
    aria = row.get("aria-label", "").strip().upper()
    for key in COUNTRY_MAP:
        if key in aria:
            return COUNTRY_MAP[key]

    # Пробуем флаг
    flag_img = row.select_one("td.flagCur img")
    if flag_img and "src" in flag_img.attrs:
        src = flag_img["src"]
        code = src.split("/")[-1].split(".")[0].upper()
        return COUNTRY_MAP.get(code, "Unknown")

    return "Unknown"

async def parse_investing_calendar():
    url = "https://www.investing.com/economic-calendar/"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                rows = soup.select("tr.js-event-item")

                events = []
                for row in rows:
                    country = extract_country_name(row)
                    importance = len(row.select(".grayFullBullishIcon"))
                    time = row.select_one(".time") or row.select_one(".date")
                    event = row.select_one(".event")
                    actual = row.select_one(".actual")
                    forecast = row.select_one(".forecast")
                    previous = row.select_one(".previous")

                    events.append({
                        "time": time.text.strip() if time else "--",
                        "country": country,
                        "event": event.text.strip() if event else "--",
                        "actual": actual.text.strip() if actual else "-",
                        "forecast": forecast.text.strip() if forecast else "-",
                        "previous": previous.text.strip() if previous else "-",
                        "importance": importance
                    })
                return events
    except Exception as e:
        print(f"⚠️ Ошибка парсинга Investing.com: {e}")
        return None

async def get_events_safe(country_filter=None, min_importance=2):
    global cached_events
    events = await parse_investing_calendar()

    if events:
        cached_events = events
        print(f"📥 Получено событий: {len(events)}")
    else:
        print("⚠️ Используем кэшированные события")
        events = cached_events

    for e in events[:5]:
        print(f"🕒 {e['time']} | 🌍 {e['country']} | 📌 {e['event']} | ⭐ {e['importance']}")

    filtered = [
        e for e in events
        if (not country_filter or e["country"] in country_filter)
        and e["importance"] >= max(min_importance - 1, 0)
    ]

    print(f"✅ Отфильтровано: {len(filtered)} событий")

    if not filtered:
        print("⚠️ Нет событий по фильтру — возвращаем заглушку")
        return [{
            "time": "--",
            "country": "N/A",
            "event": "События временно недоступны",
            "actual": "-",
            "forecast": "-",
            "previous": "-",
            "importance": "-"
        }]
    return filtered
