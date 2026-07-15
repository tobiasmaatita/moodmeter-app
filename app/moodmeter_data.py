"""Vereenvoudigde MoodMeter-woordenlijst (RULER / Yale Center for Emotional Intelligence).

Elk kwadrant combineert energie (hoog/laag) met pleasantness (onaangenaam/aangenaam):
- rood   = hoge energie, onaangenaam
- geel   = hoge energie, aangenaam
- blauw  = lage energie, onaangenaam
- groen  = lage energie, aangenaam
"""

QUADRANTS = {
    "rood": {
        "label": "Rood",
        "description": "Hoge energie, onaangenaam",
        "color": "#e5484d",
        "emotions": [
            "Woedend",
            "Paniekerig",
            "Gestrest",
            "Gespannen",
            "Nerveus",
            "Geschokt",
            "Gefrustreerd",
            "Rusteloos",
            "Geïrriteerd",
            "Angstig",
            "Overweldigd",
            "Jaloers",
        ],
    },
    "geel": {
        "label": "Geel",
        "description": "Hoge energie, aangenaam",
        "color": "#f5c211",
        "emotions": [
            "Verrast",
            "Vrolijk",
            "Uitgelaten",
            "Energiek",
            "Gemotiveerd",
            "Geïnspireerd",
            "Blij",
            "Enthousiast",
            "Optimistisch",
            "Trots",
            "Speels",
            "Zelfverzekerd",
        ],
    },
    "blauw": {
        "label": "Blauw",
        "description": "Lage energie, onaangenaam",
        "color": "#3b82f6",
        "emotions": [
            "Teleurgesteld",
            "Somber",
            "Onverschillig",
            "Pessimistisch",
            "Verdrietig",
            "Eenzaam",
            "Hopeloos",
            "Vermoeid",
            "Uitgeput",
            "Verveeld",
            "Terneergeslagen",
            "Beschaamd",
        ],
    },
    "groen": {
        "label": "Groen",
        "description": "Lage energie, aangenaam",
        "color": "#22a55e",
        "emotions": [
            "Kalm",
            "Tevreden",
            "Ontspannen",
            "Op mijn gemak",
            "Veilig",
            "Vredig",
            "Voldaan",
            "Sereen",
            "Dankbaar",
            "Nadenkend",
            "Comfortabel",
            "Rustig",
        ],
    },
}


def all_emotions_by_quadrant():
    return {key: q["emotions"] for key, q in QUADRANTS.items()}


def quadrant_color(key: str) -> str:
    return QUADRANTS.get(key, {}).get("color", "#999999")
