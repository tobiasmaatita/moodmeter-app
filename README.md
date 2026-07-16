# MoodMeter-app

Persoonlijke dagelijkse mood-check-in app, gebaseerd op de MoodMeter (RULER / Yale Center for
Emotional Intelligence). Kies elke dag één of meerdere emoties uit de vier kwadranten (energie x
pleasantness) — elk kwadrant heeft een eigen 5x5-raster van emoties, en je kunt tussen kwadranten
schakelen zonder eerder gemaakte keuzes te verliezen. Schrijf er kort bij wat er speelde, en bekijk
je geschiedenis terug.

## Lokaal draaien

```bash
uv run uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000>. Zonder `DATABASE_URL` env var gebruikt de app automatisch een
lokaal SQLite-bestand (`moodmeter.db`, staat in `.gitignore`) — handig om te testen voordat je
een echte database hebt.

## In de cloud zetten (zodat je 'm overal op je telefoon kunt gebruiken)

Je hebt hiervoor drie gratis accounts nodig. Hieronder de stappen.

### 1. Database — Supabase

1. Maak een account op [supabase.com](https://supabase.com) en maak een nieuw project aan.
2. Ga naar **Project Settings → Database → Connection string** en kies de **URI**-variant
   (meestal de "Session pooler" of "Transaction pooler" connectiestring — die werkt het best op
   Render's netwerk).
3. Kopieer die URL, die ziet er ongeveer zo uit:
   `postgresql://postgres.xxxx:[JOUW-WACHTWOORD]@aws-0-eu-central-1.pooler.supabase.com:5432/postgres`
4. Vul je databasewachtwoord in op de plek van `[JOUW-WACHTWOORD]`. Bewaar deze volledige URL
   even — die heb je zo nodig als `DATABASE_URL`.

Je hoeft zelf geen tabel aan te maken: de app doet dat automatisch bij het opstarten
(`db.init_db()` in `app/db.py`).

### 2. Code naar GitHub

```bash
git add -A
git commit -m "MoodMeter app"
git push
```

(Maak eerst een lege repo aan op GitHub en koppel die als `origin` als dat nog niet is gebeurd.)

### 3. Hosting — Render

1. Maak een account op [render.com](https://render.com) (geen creditcard nodig voor de gratis
   tier).
2. **New → Web Service**, koppel je GitHub-repo.
3. Instellingen:
   - **Runtime**: Python 3
   - **Build command**: `pip install uv && uv sync --frozen`
   - **Start command**: `uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Onder **Environment**, voeg een env var toe:
   - `DATABASE_URL` = de Supabase-connectiestring uit stap 1
5. Klik **Create Web Service**. Render bouwt en deployt de app, en geeft je een URL zoals
   `https://moodmeter-app.onrender.com`.

Let op: op de gratis tier "slaapt" de app na ongeveer 15 minuten inactiviteit. De eerstvolgende
keer dat je 'm opent duurt het laden ~30-50 seconden. Voor een dagelijkse check-in is dat geen
probleem — je opent de app toch maar een keer per dag.

### 4. Op je iPhone installeren (PWA)

1. Open de Render-URL in Safari op je iPhone.
2. Tik op het deel-icoon → **Zet op beginscherm**.
3. De app krijgt een eigen icoon en opent voortaan schermvullend, zonder Safari-balken.

## Structuur

- `app/main.py` — FastAPI-routes (`/`, `/day/{date}`, `/entries`, `/history`, `/calendar`)
- `app/db.py` — databasetabel en upsert-logica (SQLite lokaal, Postgres in productie); een
  check-in (`mood_entries`) heeft een `emotions`-kolom (JSON-lijst van `{quadrant, emotion}`) zodat
  één dag meerdere emoties kan bevatten
- `app/moodmeter_data.py` — de kwadranten en het 5x5-emotieraster van de MoodMeter, overgenomen uit
  `moodmeter-template/`
- `app/templates/` — `day_entry.html` (kwadrant-overzicht + per-kwadrant selectie, voor vandaag én
  eerdere dagen), `calendar.html`, `history.html` en de gedeelde `_nav.html`
- `app/static/` — CSS, PWA-manifest, service worker, app-iconen

## Uitbreiden

- De emotiewoorden en kleuren in `app/moodmeter_data.py` komen uit `moodmeter-template/`. Wil je
  ze aanpassen, pas dan het `QUADRANTS`-dict aan (elk kwadrant heeft een 5x5 `grid` van
  `{name, bg, text}`-cellen).
- Momenteel is er geen login — de app gaat ervan uit dat alleen jij de URL kent. Wil je dat
  afschermen, dan is een simpele wachtwoordcode (HTTP basic auth) een kleine toevoeging.
