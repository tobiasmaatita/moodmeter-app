from __future__ import annotations

import datetime as dt
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
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "quadrants": QUADRANTS,
            "today": today.isoformat(),
            "today_entry": today_entry,
        },
    )


@app.post("/entries")
def create_entry(
    quadrant: str = Form(...),
    emotion: str = Form(...),
    note: str = Form(""),
):
    if quadrant not in QUADRANTS:
        return JSONResponse({"error": "Onbekend kwadrant"}, status_code=400)
    if emotion not in QUADRANTS[quadrant]["emotions"]:
        return JSONResponse({"error": "Onbekende emotie"}, status_code=400)

    today = dt.date.today()
    db.upsert_entry(today, quadrant, emotion, note.strip())
    return JSONResponse({"ok": True, "date": today.isoformat()})


@app.get("/history")
def history(request: Request):
    entries = db.get_all_entries()
    return templates.TemplateResponse(
        request,
        "history.html",
        {"entries": entries, "quadrants": QUADRANTS},
    )
