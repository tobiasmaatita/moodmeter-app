from __future__ import annotations

import datetime as dt
import os
import uuid

from sqlalchemy import (
    JSON,
    Column,
    Date,
    DateTime,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    func,
    inspect,
    select,
    text,
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
    # Lijst van {"quadrant": ..., "emotion": ...} — een dag kan meerdere emoties bevatten.
    Column("emotions", JSON, nullable=False),
    Column("note", Text, nullable=False, default=""),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
)


def _migrate_legacy_single_emotion(conn) -> None:
    """Migreert oudere rijen (kolommen quadrant/emotion) naar de nieuwe emotions-lijst.

    Nodig omdat de productie-database al draaide met het oude schema voordat
    multi-select emoties werd toegevoegd.
    """
    inspector = inspect(conn)
    if "mood_entries" not in inspector.get_table_names():
        return  # nieuwe installatie, create_all heeft het juiste schema al gezet

    columns = {c["name"] for c in inspector.get_columns("mood_entries")}

    if "emotions" not in columns:
        col_type_ddl = mood_entries.c.emotions.type.compile(engine.dialect)
        conn.execute(text(f"ALTER TABLE mood_entries ADD COLUMN emotions {col_type_ddl}"))
        columns.add("emotions")

    if "quadrant" in columns and "emotion" in columns:
        legacy_rows = conn.execute(
            text(
                "SELECT id, quadrant, emotion FROM mood_entries "
                "WHERE emotions IS NULL AND quadrant IS NOT NULL AND emotion IS NOT NULL"
            )
        ).mappings().all()
        for row in legacy_rows:
            conn.execute(
                mood_entries.update()
                .where(mood_entries.c.id == row["id"])
                .values(emotions=[{"quadrant": row["quadrant"], "emotion": row["emotion"]}])
            )
        conn.execute(text("ALTER TABLE mood_entries DROP COLUMN quadrant"))
        conn.execute(text("ALTER TABLE mood_entries DROP COLUMN emotion"))


def init_db() -> None:
    metadata.create_all(engine)
    with engine.begin() as conn:
        _migrate_legacy_single_emotion(conn)


def upsert_entry(entry_date: dt.date, emotions: list[dict], note: str) -> None:
    with engine.begin() as conn:
        existing = conn.execute(
            select(mood_entries.c.id).where(mood_entries.c.entry_date == entry_date)
        ).first()

        if existing:
            conn.execute(
                mood_entries.update()
                .where(mood_entries.c.entry_date == entry_date)
                .values(emotions=emotions, note=note)
            )
        else:
            conn.execute(
                mood_entries.insert().values(
                    id=str(uuid.uuid4()),
                    entry_date=entry_date,
                    emotions=emotions,
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


def get_dates_with_entries(year: int, month: int) -> set[dt.date]:
    start = dt.date(year, month, 1)
    end = dt.date(year + 1, 1, 1) if month == 12 else dt.date(year, month + 1, 1)
    with engine.connect() as conn:
        rows = conn.execute(
            select(mood_entries.c.entry_date).where(
                mood_entries.c.entry_date >= start,
                mood_entries.c.entry_date < end,
            )
        ).all()
    return {row[0] for row in rows}
