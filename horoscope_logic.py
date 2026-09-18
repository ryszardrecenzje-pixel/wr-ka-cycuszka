import json
import random
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any

DATA_DIR = Path(__file__).parent.parent / "data" / "horoscopes"

ZODIAC_SIGNS = {
    "baran": {"name": "Baran", "emoji": "♈", "element": "Ogień", "dates": "21.03 – 19.04"},
    "byk": {"name": "Byk", "emoji": "♉", "element": "Ziemia", "dates": "20.04 – 20.05"},
    "bliznieta": {"name": "Bliźnięta", "emoji": "♊", "element": "Powietrze", "dates": "21.05 – 20.06"},
    "rak": {"name": "Rak", "emoji": "♋", "element": "Woda", "dates": "21.06 – 22.07"},
    "lew": {"name": "Lew", "emoji": "♌", "element": "Ogień", "dates": "23.07 – 22.08"},
    "panna": {"name": "Panna", "emoji": "♍", "element": "Ziemia", "dates": "23.08 – 22.09"},
    "waga": {"name": "Waga", "emoji": "♎", "element": "Powietrze", "dates": "23.09 – 22.10"},
    "skorpion": {"name": "Skorpion", "emoji": "♏", "element": "Woda", "dates": "23.10 – 21.11"},
    "strzelec": {"name": "Strzelec", "emoji": "♐", "element": "Ogień", "dates": "22.11 – 21.12"},
    "koziorozec": {"name": "Koziorożec", "emoji": "♑", "element": "Ziemia", "dates": "22.12 – 19.01"},
    "wodnik": {"name": "Wodnik", "emoji": "♒", "element": "Powietrze", "dates": "20.01 – 18.02"},
    "ryby": {"name": "Ryby", "emoji": "♓", "element": "Woda", "dates": "19.02 – 20.03"},
}

def load_sign_data(sign_key: str) -> Dict[str, Any]:
    path = DATA_DIR / f"{sign_key}.json"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_lucky_number() -> int:
    return random.randint(1, 99)

def get_lucky_color() -> str:
    colors = [
        "Fiolet", "Złoto", "Srebro", "Granat", "Bordeaux",
        "Turkus", "Szmaragd", "Bursztyn", "Perłowy", "Czerń"
    ]
    return random.choice(colors)

def generate_horoscope(sign_key: str, period: str = "dzienny") -> Dict[str, Any]:
    data = load_sign_data(sign_key)
    if not data:
        return {"error": "Brak danych dla tego znaku."}

    templates = data.get(period, data.get("dzienny", {}))
    if not templates:
        return {"error": "Brak szablonów dla wybranego okresu."}

    # Losujemy warianty tekstów
    general = random.choice(templates.get("ogolna", ["Energia dnia sprzyja refleksji."]))
    love = random.choice(templates.get("milosc", ["W relacjach panuje harmonia."]))
    career = random.choice(templates.get("kariera", ["Skup się na konkretnych zadaniach."]))
    health = random.choice(templates.get("zdrowie", ["Dbaj o regenerację."]))
    advice = random.choice(templates.get("rada", ["Zaufaj swojej intuicji."]))

    sign_info = ZODIAC_SIGNS.get(sign_key, {})

    return {
        "sign_key": sign_key,
        "sign_name": sign_info.get("name", sign_key),
        "emoji": sign_info.get("emoji", "✨"),
        "element": sign_info.get("element", ""),
        "dates": sign_info.get("dates", ""),
        "period": period,
        "date": datetime.now().strftime("%d.%m.%Y"),
        "general": general,
        "love": love,
        "career": career,
        "health": health,
        "advice": advice,
        "lucky_number": get_lucky_number(),
        "lucky_color": get_lucky_color(),
    }

def get_period_label(period: str) -> str:
    labels = {
        "dzienny": "Horoskop dzienny",
        "tygodniowy": "Horoskop tygodniowy",
        "miesieczny": "Horoskop miesięczny"
    }
    return labels.get(period, period)
