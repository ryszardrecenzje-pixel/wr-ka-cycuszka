import json
import random
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

DATA_PATH = Path(__file__).parent.parent / "data" / "tarot_cards.json"

def load_tarot_deck() -> List[Dict[str, Any]]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def draw_cards(num: int, allow_reversed: bool = True) -> List[Dict[str, Any]]:
    deck = load_tarot_deck()
    drawn = random.sample(deck, num)
    result = []
    for card in drawn:
        is_reversed = allow_reversed and random.random() < 0.35
        result.append({
            "id": card["id"],
            "name": card["name"],
            "name_pl": card["name_pl"],
            "arcana": card["arcana"],
            "suit": card.get("suit"),
            "upright": card["upright"],
            "reversed": card["reversed"],
            "is_reversed": is_reversed,
            "meaning": card["reversed"] if is_reversed else card["upright"]
        })
    return result

SPREADS = {
    "1_karta": {
        "name": "Jedna karta",
        "positions": ["Twoja odpowiedź"],
        "description": "Szybka, klarowna odpowiedź na pytanie. Idealna, gdy potrzebujesz jednego wyraźnego wskazania."
    },
    "3_karty": {
        "name": "Trzy karty",
        "positions": ["Przeszłość", "Teraźniejszość", "Przyszłość"],
        "description": "Klasyczny układ pokazujący ciąg zdarzeń: skąd przychodzisz, gdzie jesteś i dokąd zmierzasz."
    },
    "krzyz_celtycki": {
        "name": "Krzyż Celtycki",
        "positions": [
            "Sytuacja obecna",
            "Wyzwanie / przeszkoda",
            "Daleka przeszłość",
            "Niedawna przeszłość",
            "Możliwa przyszłość",
            "Bliska przyszłość",
            "Twoje podejście",
            "Wpływ otoczenia",
            "Nadzieje i obawy",
            "Ostateczny wynik"
        ],
        "description": "Głęboki, 10-kartowy układ dający pełny obraz sytuacji — od korzeni po możliwy rezultat."
    }
}

POSITION_GUIDANCE = {
    "Twoja odpowiedź": "Ta karta jest bezpośrednią odpowiedzią na Twoje pytanie. Przyjmij ją jako wskazówkę, nie wyrok.",
    "Przeszłość": "Pokazuje wpływy i wydarzenia, które ukształtowały obecną sytuację. To fundament, z którego wyrasta teraz.",
    "Teraźniejszość": "Opisuje energię chwili obecnej — to, co dzieje się teraz i co wymaga Twojej uwagi.",
    "Przyszłość": "Wskazuje najbardziej prawdopodobny kierunek, jeśli obecne energie pozostaną bez zmian. Nie jest to fatum — możesz go kształtować.",
    "Sytuacja obecna": "Rdzeń sprawy. To, co jest w centrum Twojego pytania w tej chwili.",
    "Wyzwanie / przeszkoda": "Siła, która krzyżuje drogę lub wymaga przepracowania. Często to klucz do zmiany.",
    "Daleka przeszłość": "Głębsze korzenie sytuacji — wzorce, doświadczenia lub decyzje z dalszej przeszłości.",
    "Niedawna przeszłość": "Niedawne wydarzenia, które bezpośrednio doprowadziły do obecnego stanu.",
    "Możliwa przyszłość": "Jeden z możliwych scenariuszy — potencjalny rozwój, jeśli podążysz obecną ścieżką.",
    "Bliska przyszłość": "To, co może wydarzyć się w najbliższym czasie. Warto być czujnym.",
    "Twoje podejście": "Jak Ty sam podchodzisz do sytuacji — Twoja postawa, przekonania, sposób działania.",
    "Wpływ otoczenia": "Ludzie, okoliczności i energie zewnętrzne, które na Ciebie oddziałują.",
    "Nadzieje i obawy": "To, czego pragniesz i czego się boisz — często dwie strony tej samej monety.",
    "Ostateczny wynik": "Najbardziej prawdopodobny rezultat przy obecnym układzie sił. Pamiętaj: karty doradzają, nie rozkazują."
}

def create_reading(spread_key: str, question: str = "") -> Dict[str, Any]:
    spread = SPREADS[spread_key]
    cards = draw_cards(len(spread["positions"]))
    reading = {
        "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "timestamp": datetime.now().isoformat(),
        "spread": spread_key,
        "spread_name": spread["name"],
        "question": question.strip() or "Brak pytania",
        "cards": []
    }
    for i, card in enumerate(cards):
        pos = spread["positions"][i]
        reading["cards"].append({
            **card,
            "position": pos,
            "position_guidance": POSITION_GUIDANCE.get(pos, "Ta pozycja wnosi ważny kontekst do odczytu.")
        })
    return reading

def get_synthesis(cards: List[Dict]) -> str:
    reversed_count = sum(1 for c in cards if c["is_reversed"])
    major_count = sum(1 for c in cards if c["arcana"] == "Wielkie")
    total = len(cards)

    parts = []

    # Energia ogólna
    if reversed_count >= total * 0.6:
        parts.append(
            "W odczycie dominuje energia odwrócona. Może to oznaczać blokady, opóźnienia, "
            "wewnętrzny opór lub potrzebę zmiany perspektywy. Zamiast forsować działanie, "
            "warto najpierw zrozumieć, co Cię hamuje."
        )
    elif reversed_count == 0:
        parts.append(
            "Wszystkie karty wypadły w pozycji prostej. Energia płynie swobodnie i sprzyja działaniu. "
            "To dobry moment, by podejmować decyzje i iść naprzód z większą pewnością."
        )
    else:
        parts.append(
            "Odczyt jest zrównoważony — mieszają się siły wspierające i te, które wymagają uwagi. "
            "Nie wszystko pójdzie gładko, ale masz wystarczająco dużo zasobów, by poradzić sobie z wyzwaniami."
        )

    # Wielkie Arkana
    if major_count >= max(1, total * 0.5):
        parts.append(
            "Silna obecność Wielkich Arkanów wskazuje na ważne, często karmiczne lub przełomowe wydarzenia. "
            "To nie jest zwykła codzienna sprawa — tu chodzi o głębszą lekcję i transformację."
        )
    elif major_count == 0:
        parts.append(
            "Przewaga Małych Arkanów sugeruje, że sytuacja dotyczy głównie codziennych spraw, "
            "konkretnych działań i praktycznych decyzji. Skup się na tym, co możesz zrobić tu i teraz."
        )
    else:
        parts.append(
            "Obecność zarówno Wielkich, jak i Małych Arkanów pokazuje, że duże tematy życiowe "
            "przenikają się z codziennymi wyborami. Małe kroki prowadzą do większych zmian."
        )

    # Rada końcowa
    if reversed_count > total / 2:
        parts.append(
            "Rada: zwolnij, przyjrzyj się swoim lękom i przekonaniom. Czasem największą siłą jest "
            "gotowość, by puścić to, co już nie służy."
        )
    else:
        parts.append(
            "Rada: zaufaj procesowi, ale nie działaj na ślepo. Karty pokazują potencjał — "
            "Twoja świadoma decyzja zamienia go w rzeczywistość."
        )

    return " ".join(parts)


def answer_followup(question: str, cards: List[Dict]) -> str:
    """Generuje odpowiedź na pytanie dodatkowe na podstawie wylosowanych kart."""
    if not question.strip():
        return "Zadaj konkretne pytanie, a karty podpowiedzą."

    q = question.lower().strip()

    # Wybierz 1-2 najbardziej "pasujące" karty (losowo z puli, ale z kontekstem)
    selected = random.sample(cards, min(2, len(cards)))

    intro_options = [
        "Patrząc na karty z Twojego odczytu,",
        "W kontekście tego, co już wypadło,",
        "Karty, które masz przed sobą, podpowiadają,",
        "Odnosząc się do energii obecnego rozkładu,",
    ]
    intro = random.choice(intro_options)

    card_parts = []
    for c in selected:
        orient = "w pozycji odwróconej" if c["is_reversed"] else "w pozycji prostej"
        card_parts.append(
            f"**{c['name_pl']}** ({c['position']}, {orient}) mówi: {c['meaning']}"
        )

    # Dopasowanie tonu do typu pytania
    if any(w in q for w in ["miłość", "związek", "partner", "uczuc", "serc", "relacj"]):
        theme = (
            "W sprawach serca kluczowe jest szczere spojrzenie na siebie i drugą osobę. "
            "Nie uciekaj od emocji — one są teraz Twoim przewodnikiem."
        )
    elif any(w in q for w in ["prac", "karier", "pieniądz", "finans", "zawod", "biznes"]):
        theme = (
            "W sferze zawodowej i materialnej liczy się teraz konkret i konsekwencja. "
            "Unikaj pochopnych decyzji, ale nie bój się też zrobić kroku, gdy pojawia się okazja."
        )
    elif any(w in q for w in ["co robić", "jak", "czy powinien", "czy mam", "decyz"]):
        theme = (
            "Decyzja, którą rozważasz, wymaga połączenia intuicji z rozsądkiem. "
            "Karty nie zdejmują z Ciebie odpowiedzialności — one ją rozjaśniają."
        )
    elif any(w in q for w in ["kiedy", "czas", "jak długo", "termin"]):
        theme = (
            "Czas w tarocie jest płynny. Zamiast szukać konkretnej daty, zwróć uwagę na warunki, "
            "które muszą się spełnić, zanim coś dojrzeje."
        )
    else:
        theme = (
            "Odpowiedź leży na przecięciu tego, co już wiesz, i tego, na co karty zwracają uwagę. "
            "Nie ignoruj subtelnym sygnałów — często są ważniejsze niż głośne wydarzenia."
        )

    closing_options = [
        "Przyjmij tę wskazówkę z otwartością i sprawdź, jak rezonuje z Twoim wewnętrznym głosem.",
        "Pamiętaj: karty oświetlają ścieżkę, ale to Ty stawiasz na niej kroki.",
        "Zatrzymaj się na chwilę z tą odpowiedzią — czasem najwięcej mówi cisza po pytaniu.",
    ]
    closing = random.choice(closing_options)

    answer = (
        f"{intro}\n\n"
        + "\n\n".join(card_parts)
        + f"\n\n{theme}\n\n*{closing}*"
    )
    return answer
