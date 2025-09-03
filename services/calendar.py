from bs4 import BeautifulSoup
import aiohttp
from datetime import datetime, timedelta
import pytz

KYIV_TZ = pytz.timezone("Europe/Kyiv")
cached_events = []

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
                    raw_datetime = row.get("data-event-datetime")
                    try:
                        dt_utc = datetime.strptime(raw_datetime, "%Y/%m/%d %H:%M:%S")
                        dt_utc = pytz.utc.localize(dt_utc)
                        dt_local = dt_utc.astimezone(KYIV_TZ)
                        event_date = dt_local.date()
                        event_time = dt_local.time()
                    except Exception as e:
                        print(f"⚠️ Ошибка парсинга времени: {raw_datetime} → {e}")
                        dt_local = None
                        event_date = None
                        event_time = None

                    event = row.select_one(".event")
                    actual = row.select_one("td[data-column='actual']") or row.select_one(".actual")
                    forecast = row.select_one("td[data-column='forecast']") or row.select_one(".forecast")
                    previous = row.select_one("td[data-column='previous']") or row.select_one(".previous")
                    importance = len(row.select(".grayFullBullishIcon"))

                    event_text = event.text.strip() if event else "--"
                    actual_text = actual.text.strip() if actual else "-"
                    forecast_text = forecast.text.strip() if forecast else "-"
                    previous_text = previous.text.strip() if previous else "-"

                    print(f"🧪 {raw_datetime} | {event_text}")
                    print(f"    Факт: {actual_text} | Прогноз: {forecast_text} | Пред: {previous_text}")

                    events.append({
                        "date": event_date,
                        "time": event_time.strftime("%H:%M") if event_time else "--",
                        "datetime": dt_local,
                        "event": event_text,
                        "actual": actual_text,
                        "forecast": forecast_text,
                        "previous": previous_text,
                        "importance": importance
                    })
                print(f"✅ Всего событий спарсено: {len(events)}")
                return events
    except Exception as e:
        print(f"❌ Ошибка загрузки календаря: {e}")
        return None

async def get_events_by_date(mode="today"):
    global cached_events
    now = datetime.now(KYIV_TZ)

    need_refresh = (
        not cached_events or
        any(e["datetime"] and e["datetime"] < now and e["actual"] == "-" for e in cached_events)
    )

    if need_refresh:
        print("🔁 Обновление кэша событий...")
        events = await parse_investing_calendar()
        if events:
            cached_events = events
    else:
        print("📦 Используем кэш событий")

    today = now.date()
    tomorrow = today + timedelta(days=1)
    week_later = today + timedelta(days=7)

    def match(e):
        if not e["date"]:
            return False
        if mode == "today":
            return e["date"] == today
        elif mode == "tomorrow":
            return e["date"] == tomorrow
        elif mode == "week":
            return today <= e["date"] <= week_later
        return False

    filtered = [e for e in cached_events if match(e)]
    print(f"📅 Отфильтровано ({mode}): {len(filtered)} событий")

    if not filtered:
        return [{
            "time": "--",
            "event": "События на выбранную дату отсутствуют",
            "actual": "-",
            "forecast": "-",
            "previous": "-",
            "importance": "-",
            "datetime": None
        }]
    return filtered

async def get_upcoming_important_events():
    now = datetime.now(KYIV_TZ)
    events = await get_events_by_date("today")
    upcoming = []

    for e in events:
        dt = e.get("datetime")
        if dt and dt >= now and e["importance"] >= 2:
            upcoming.append(e)

    print(f"🔔 Ближайшие важные события: {len(upcoming)}")
    return upcoming
