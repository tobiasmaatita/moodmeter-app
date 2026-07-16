"""MoodMeter-woordenlijst gebaseerd op de Yale RULER Mood Meter (zie moodmeter-template/).

Elk kwadrant combineert energie (hoog/laag) met plezierigheid (onaangenaam/aangenaam)
en bevat een 5x5 raster van emoties, van mild (dicht bij het midden) tot intens (buitenrand),
conform de originele Mood Meter-poster.
"""

QUADRANTS = {
    "rood": {
        "label": "Rood",
        "description": "Hoge energie, onaangenaam",
        "color": "#CC0622",
        "grid": [
            [{"name": "Woedend", "bg": "#CC0622", "text": "#ffffff"}, {"name": "In paniek", "bg": "#CC0622", "text": "#ffffff"}, {"name": "Gestrest", "bg": "#E7457F", "text": "#ffffff"}, {"name": "Zenuwachtig", "bg": "#F5ADCC", "text": "#12141a"}, {"name": "Geschokt", "bg": "#FBE1EB", "text": "#12141a"}],
            [{"name": "Pissig", "bg": "#CC0622", "text": "#ffffff"}, {"name": "Driftig", "bg": "#CC0622", "text": "#ffffff"}, {"name": "Gefrustreerd", "bg": "#E7457F", "text": "#ffffff"}, {"name": "Gespannen", "bg": "#F5ADCC", "text": "#12141a"}, {"name": "Verbijsterd", "bg": "#FBE1EB", "text": "#12141a"}],
            [{"name": "Verbolgen", "bg": "#E7457F", "text": "#ffffff"}, {"name": "Bang", "bg": "#E7457F", "text": "#ffffff"}, {"name": "Boos", "bg": "#E7457F", "text": "#ffffff"}, {"name": "Nerveus", "bg": "#F5ADCC", "text": "#12141a"}, {"name": "Rusteloos", "bg": "#FBE1EB", "text": "#12141a"}],
            [{"name": "Angstig", "bg": "#F5ADCC", "text": "#12141a"}, {"name": "Ongerust", "bg": "#F5ADCC", "text": "#12141a"}, {"name": "Zorgelijk", "bg": "#F5ADCC", "text": "#12141a"}, {"name": "Geïrriteerd", "bg": "#F5ADCC", "text": "#12141a"}, {"name": "Geërgerd", "bg": "#FBE1EB", "text": "#12141a"}],
            [{"name": "Afkerig", "bg": "#FBE1EB", "text": "#12141a"}, {"name": "Onrustig", "bg": "#FBE1EB", "text": "#12141a"}, {"name": "Bezorgd", "bg": "#FBE1EB", "text": "#12141a"}, {"name": "Ongemakkelijk", "bg": "#FBE1EB", "text": "#12141a"}, {"name": "Geraakt", "bg": "#FBE1EB", "text": "#12141a"}],
        ],
    },
    "geel": {
        "label": "Geel",
        "description": "Hoge energie, aangenaam",
        "color": "#F7F703",
        "grid": [
            [{"name": "Verrast", "bg": "#FAFEC2", "text": "#12141a"}, {"name": "Vrolijk", "bg": "#FAFEC2", "text": "#12141a"}, {"name": "Feeststemming", "bg": "#F4FE90", "text": "#12141a"}, {"name": "Opgewonden", "bg": "#F7F703", "text": "#12141a"}, {"name": "In extase", "bg": "#F7F703", "text": "#12141a"}],
            [{"name": "Hyper", "bg": "#FAFEC2", "text": "#12141a"}, {"name": "Opgewekt", "bg": "#FAFEC2", "text": "#12141a"}, {"name": "Gemotiveerd", "bg": "#F4FE90", "text": "#12141a"}, {"name": "Geïnspireerd", "bg": "#F7F703", "text": "#12141a"}, {"name": "Verrukt", "bg": "#F7F703", "text": "#12141a"}],
            [{"name": "Opgeladen", "bg": "#FAFEC2", "text": "#12141a"}, {"name": "Levendig", "bg": "#FAFEC2", "text": "#12141a"}, {"name": "Opgetogen", "bg": "#F4FE90", "text": "#12141a"}, {"name": "Optimistisch", "bg": "#F4FE90", "text": "#12141a"}, {"name": "Enthousiast", "bg": "#F4FE90", "text": "#12141a"}],
            [{"name": "Verheugd", "bg": "#FAFEC2", "text": "#12141a"}, {"name": "Gefocust", "bg": "#FAFEC2", "text": "#12141a"}, {"name": "Blij", "bg": "#FAFEC2", "text": "#12141a"}, {"name": "Trots", "bg": "#FAFEC2", "text": "#12141a"}, {"name": "Ontroerd", "bg": "#FAFEC2", "text": "#12141a"}],
            [{"name": "Monter", "bg": "#FAFEC2", "text": "#12141a"}, {"name": "Vreugdevol", "bg": "#FAFEC2", "text": "#12141a"}, {"name": "Hoopvol", "bg": "#FAFEC2", "text": "#12141a"}, {"name": "Speels", "bg": "#FDFFE7", "text": "#12141a"}, {"name": "Gelukkig", "bg": "#FDFFE7", "text": "#12141a"}],
        ],
    },
    "blauw": {
        "label": "Blauw",
        "description": "Lage energie, onaangenaam",
        "color": "#0B76A0",
        "grid": [
            [{"name": "Walgend", "bg": "#CAEEFB", "text": "#12141a"}, {"name": "Somber", "bg": "#CAEEFB", "text": "#12141a"}, {"name": "Teleurgesteld", "bg": "#CAEEFB", "text": "#12141a"}, {"name": "Triest", "bg": "#CAEEFB", "text": "#12141a"}, {"name": "Apathisch", "bg": "#CAEEFB", "text": "#12141a"}],
            [{"name": "Pessimistisch", "bg": "#96DCF8", "text": "#12141a"}, {"name": "Chagrijnig", "bg": "#96DCF8", "text": "#12141a"}, {"name": "Ontmoedigd", "bg": "#96DCF8", "text": "#12141a"}, {"name": "Verdrietig", "bg": "#96DCF8", "text": "#12141a"}, {"name": "Verveeld", "bg": "#CAEEFB", "text": "#12141a"}],
            [{"name": "Vervreemd", "bg": "#61CBF4", "text": "#12141a"}, {"name": "Ellendig", "bg": "#61CBF4", "text": "#12141a"}, {"name": "Eenzaam", "bg": "#61CBF4", "text": "#12141a"}, {"name": "Verslagen", "bg": "#96DCF8", "text": "#12141a"}, {"name": "Moe", "bg": "#CAEEFB", "text": "#12141a"}],
            [{"name": "Moedeloos", "bg": "#0B76A0", "text": "#ffffff"}, {"name": "Depressief", "bg": "#0B76A0", "text": "#ffffff"}, {"name": "Nors", "bg": "#61CBF4", "text": "#12141a"}, {"name": "Uitgeput", "bg": "#96DCF8", "text": "#12141a"}, {"name": "Afgemat", "bg": "#CAEEFB", "text": "#12141a"}],
            [{"name": "Wanhopig", "bg": "#0B76A0", "text": "#ffffff"}, {"name": "Hopeloos", "bg": "#0B76A0", "text": "#ffffff"}, {"name": "Troosteloos", "bg": "#61CBF4", "text": "#12141a"}, {"name": "Opgebrand", "bg": "#96DCF8", "text": "#12141a"}, {"name": "Leeggezogen", "bg": "#CAEEFB", "text": "#12141a"}],
        ],
    },
    "groen": {
        "label": "Groen",
        "description": "Lage energie, aangenaam",
        "color": "#3B7D23",
        "grid": [
            [{"name": "Op je gemak", "bg": "#D9F2D0", "text": "#12141a"}, {"name": "Meegaand", "bg": "#D9F2D0", "text": "#12141a"}, {"name": "Content", "bg": "#D9F2D0", "text": "#12141a"}, {"name": "Liefdevol", "bg": "#D9F2D0", "text": "#12141a"}, {"name": "Vervuld", "bg": "#D9F2D0", "text": "#12141a"}],
            [{"name": "Kalm", "bg": "#D9F2D0", "text": "#12141a"}, {"name": "Veilig", "bg": "#B4E5A2", "text": "#12141a"}, {"name": "Bevredigd", "bg": "#B4E5A2", "text": "#12141a"}, {"name": "Dankbaar", "bg": "#B4E5A2", "text": "#12141a"}, {"name": "Bewogen", "bg": "#B4E5A2", "text": "#12141a"}],
            [{"name": "Ontspannen", "bg": "#D9F2D0", "text": "#12141a"}, {"name": "Meditatief", "bg": "#B4E5A2", "text": "#12141a"}, {"name": "Rustig", "bg": "#8ED973", "text": "#12141a"}, {"name": "Gezegend", "bg": "#8ED973", "text": "#12141a"}, {"name": "In evenwicht", "bg": "#8ED973", "text": "#12141a"}],
            [{"name": "Mild", "bg": "#D9F2D0", "text": "#12141a"}, {"name": "Bedachtzaam", "bg": "#B4E5A2", "text": "#12141a"}, {"name": "Vredig", "bg": "#8ED973", "text": "#12141a"}, {"name": "Comfortabel", "bg": "#3B7D23", "text": "#ffffff"}, {"name": "Zorgeloos", "bg": "#3B7D23", "text": "#ffffff"}],
            [{"name": "Slaperig", "bg": "#D9F2D0", "text": "#12141a"}, {"name": "Voldaan", "bg": "#B4E5A2", "text": "#12141a"}, {"name": "Senang", "bg": "#8ED973", "text": "#12141a"}, {"name": "Behaaglijk", "bg": "#3B7D23", "text": "#ffffff"}, {"name": "Sereen", "bg": "#3B7D23", "text": "#ffffff"}],
        ],
    },
}


def all_emotions_by_quadrant():
    return {
        key: [cell["name"] for row in q["grid"] for cell in row]
        for key, q in QUADRANTS.items()
    }


def quadrant_color(key: str) -> str:
    return QUADRANTS.get(key, {}).get("color", "#999999")
