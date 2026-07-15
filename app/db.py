from __future__ import annotations

import datetime as dt
import os

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    func,
    select,
)

def _resolve_database_url() -> str:
    url = os.environ.get("DATABASE_URL", "sqlite:///./moodmeter.db")
    # Supabase/Render geven vaak "postgresql://" of "postgres://" terug;
    # SQLAlchemy heeft het psycopg3-dialect nodig om die te gebruiken.
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://") and "+psycopg" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


DATABASE_URL = _resolve_database_url()

engine = create_engine(DATABASE_URL, echo=False, future=True)

metadata = MetaData()

mood_entries = Table(
    "mood_entries",
    metadata,
    Column("id", String, primary_key=True),
    Column("entry_date", Date, nullable=False, unique=True),
    Column("quadrant", String, nullable=False),
    Column("emotion", String, nullable=False),
    Column("note", Text, nullable=False, default=""),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
)


def init_db() -> None:
    metadata.create_all(engine)


def upsert_entry(entry_date: dt.date, quadrant: str, emotion: str, note: str) -> None:
    import uuid

    with engine.begin() as conn:
        existing = conn.execute(
            select(mood_entries.c.id).where(mood_entries.c.entry_date == entry_date)
        ).first()

        if existing:
            conn.execute(
                mood_entries.update()
                .where(mood_entries.c.entry_date == entry_date)
                .values(quadrant=quadrant, emotion=emotion, note=note)
            )
        else:
            conn.execute(
                mood_entries.insert().values(
                    id=str(uuid.uuid4()),
                    entry_date=entry_date,
                    quadrant=quadrant,
                    emotion=emotion,
                    note=note,
                )
            )


def get_all_entries() -> list[dict]:
    with engine.connect() as conn:
        rows = conn.execute(
            select(mood_entries).order_by(mood_entries.c.entry_date.desc())
        ).mappings().all()
    return [dict(row) for row in rows]


def get_entry_for_date(entry_date: dt.date) -> dict | None:
    with engine.connect() as conn:
        row = conn.execute(
            select(mood_entries).where(mood_entries.c.entry_date == entry_date)
        ).mappings().first()
    return dict(row) if row else None
