from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import db
from app.moodmeter_data import QUADRANTS

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="MoodMeter")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.on_event("startup")
def on_startup() -> None:
    db.init_db()


@app.get("/")
def homescreen(request: Request):
    today = dt.date.today()
    today_entry = db.get_entry_for_date(today)
    today_emotions = today_entry["emotions"] if today_entry else []
    today_note = today_entry["note"] if today_entry else ""
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "quadrants": QUADRANTS,
            "today": today.isoformat(),
            "today_emotions": today_emotions,
            "today_emotions_json": json.dumps(today_emotions),
            "today_note": today_note,
        },
    )


@app.post("/entries")
def create_entry(
    emotions: str = Form(...),
    note: str = Form(""),
):
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

    today = dt.date.today()
    db.upsert_entry(today, cleaned, note.strip())
    return JSONResponse({"ok": True, "date": today.isoformat()})


@app.get("/history")
def history(request: Request):
    entries = db.get_all_entries()
    return templates.TemplateResponse(
        request,
        "history.html",
        {"entries": entries, "quadrants": QUADRANTS},
    )
