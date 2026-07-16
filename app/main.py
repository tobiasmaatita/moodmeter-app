from __future__ import annotations

import calendar
import datetime as dt
import json
from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import db
from app.moodmeter_data import QUADRANTS

BASE_DIR = Path(__file__).resolve().parent

MONTHS_NL = [
    "januari", "februari", "maart", "april", "mei", "juni",
    "juli", "augustus", "september", "oktober", "november", "december",
]
WEEKDAYS_NL_SHORT = ["Ma", "Di", "Wo", "Do", "Vr", "Za", "Zo"]
WEEKDAYS_NL_FULL = [
    "maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag",
]

app = FastAPI(title="MoodMeter")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.on_event("startup")
def on_startup() -> None:
    db.init_db()


def _format_date_label(entry_date: dt.date) -> str:
    weekday = WEEKDAYS_NL_FULL[entry_date.weekday()]
    month = MONTHS_NL[entry_date.month - 1]
    return f"{weekday} {entry_date.day} {month} {entry_date.year}"


def _render_day_entry(request: Request, entry_date: dt.date):
    today = dt.date.today()
    is_today = entry_date == today
    entry = db.get_entry_for_date(entry_date)
    existing_emotions = entry["emotions"] if entry else []
    existing_note = entry["note"] if entry else ""
    return templates.TemplateResponse(
        request,
        "day_entry.html",
        {
            "quadrants": QUADRANTS,
            "entry_date": entry_date.isoformat(),
            "entry_date_json": json.dumps(entry_date.isoformat()),
            "entry_date_label": "Vandaag" if is_today else _format_date_label(entry_date),
            "is_today": is_today,
            "existing_emotions": existing_emotions,
            "existing_emotions_json": json.dumps(existing_emotions),
            "existing_note": existing_note,
            "active_tab": "vandaag" if is_today else "kalender",
        },
    )


@app.get("/")
def homescreen(request: Request):
    return _render_day_entry(request, dt.date.today())


@app.get("/day/{date_str}")
def day_entry(request: Request, date_str: str):
    try:
        entry_date = dt.date.fromisoformat(date_str)
    except ValueError:
        raise HTTPException(status_code=404, detail="Ongeldige datum")

    if entry_date > dt.date.today():
        raise HTTPException(status_code=404, detail="Je kunt geen mood voor de toekomst invullen")

    return _render_day_entry(request, entry_date)


@app.post("/entries")
def create_entry(
    date: str = Form(...),
    emotions: str = Form(...),
    note: str = Form(""),
):
    try:
        entry_date = dt.date.fromisoformat(date)
    except ValueError:
        return JSONResponse({"error": "Ongeldige datum"}, status_code=400)

    if entry_date > dt.date.today():
        return JSONResponse({"error": "Je kunt geen mood voor de toekomst invullen"}, status_code=400)

    try:
        selections = json.loads(emotions)
    except json.JSONDecodeError:
        return JSONResponse({"error": "Ongeldige emotieselectie"}, status_code=400)

    if not isinstance(selections, list) or not selections:
        return JSONResponse({"error": "Kies minstens één emotie"}, status_code=400)

    cleaned = []
    seen = set()
    for item in selections:
        if not isinstance(item, dict):
            return JSONResponse({"error": "Ongeldige emotieselectie"}, status_code=400)
        quadrant = item.get("quadrant")
        emotion = item.get("emotion")
        if quadrant not in QUADRANTS or emotion not in QUADRANTS[quadrant]["emotions"]:
            return JSONResponse({"error": "Onbekende emotie"}, status_code=400)
        key = (quadrant, emotion)
        if key in seen:
            continue
        seen.add(key)
        cleaned.append({"quadrant": quadrant, "emotion": emotion})

    db.upsert_entry(entry_date, cleaned, note.strip())
    return JSONResponse({"ok": True, "date": entry_date.isoformat()})


@app.get("/history")
def history(request: Request):
    entries = db.get_all_entries()
    return templates.TemplateResponse(
        request,
        "history.html",
        {"entries": entries, "quadrants": QUADRANTS, "active_tab": "geschiedenis"},
    )


@app.get("/calendar")
def calendar_view(request: Request, month: str | None = None):
    today = dt.date.today()

    year, mon = today.year, today.month
    if month:
        try:
            year, mon = (int(part) for part in month.split("-"))
            dt.date(year, mon, 1)
        except (ValueError, TypeError):
            year, mon = today.year, today.month

    first_of_month = dt.date(year, mon, 1)
    weeks = calendar.Calendar(firstweekday=0).monthdatescalendar(year, mon)
    filled_dates = db.get_dates_with_entries(year, mon)

    prev_month_date = (first_of_month - dt.timedelta(days=1)).replace(day=1)
    next_month_date = (first_of_month + dt.timedelta(days=32)).replace(day=1)
    next_disabled = (next_month_date.year, next_month_date.month) > (today.year, today.month)

    return templates.TemplateResponse(
        request,
        "calendar.html",
        {
            "weeks": weeks,
            "month_label": f"{MONTHS_NL[mon - 1]} {year}",
            "weekday_labels": WEEKDAYS_NL_SHORT,
            "current_month": mon,
            "today": today,
            "filled_dates": filled_dates,
            "prev_month": f"{prev_month_date.year:04d}-{prev_month_date.month:02d}",
            "next_month": f"{next_month_date.year:04d}-{next_month_date.month:02d}",
            "next_disabled": next_disabled,
            "active_tab": "kalender",
        },
    )
