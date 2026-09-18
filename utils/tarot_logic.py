import json
import random
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

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

# --- Wykrywanie tematu pytania ---
THEME_KEYWORDS = {
    "milosc": ["miłość", "miłości", "związek", "związku", "partner", "partnerka", "mąż", "żona",
               "chłopak", "dziewczyna", "uczuc", "serc", "relacj", "randk", "romans", "rozstani"],
    "kariera": ["prac", "karier", "zawod", "szef", "firm", "biznes", "pieniądz", "finans",
                "pensj", "zarob", "stanowisk", "projekt", "klient"],
    "zdrowie": ["zdrow", "chorob", "ból", "lekar", "terap", "sen", "stres", "energia", "samopocz"],
    "decyzja": ["czy powinien", "czy mam", "decyz", "wybór", "wyboru", "co robić", "jak postąpić",
                "czy warto", "czy zostawić", "czy zmienić"],
    "czas": ["kiedy", "jak długo", "termin", "czas", "wkrótce", "kiedyś"],
    "rozwoj": ["rozwoj", "rozwoju", "ścieżk", "cel", "sens", "duchow", "zmian", "transform"],
}

def detect_theme(question: str) -> str:
    if not question or question == "Brak pytania":
        return "ogolny"
    q = question.lower()
    scores = {theme: sum(1 for kw in kws if kw in q) for theme, kws in THEME_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "ogolny"


THEME_LENSES = {
    "milosc": {
        "intro": [
            "W sprawach serca ten rozkład mówi wyraźnie.",
            "Patrząc przez pryzmat relacji i uczuć,",
            "Jeśli chodzi o bliskość i związek,",
        ],
        "advice": [
            "Najważniejsza rada: nie uciekaj od szczerości — wobec siebie i drugiej osoby.",
            "Relacja rośnie tam, gdzie jest miejsce na prawdę, nie tylko na nadzieję.",
            "Zanim cokolwiek zdecydujesz, sprawdź, czy działasz z miłości, czy z lęku przed samotnością.",
        ],
    },
    "kariera": {
        "intro": [
            "W kontekście pracy i materialnej stabilności układ układa się tak:",
            "Jeśli pytasz o karierę lub finanse,",
            "W sferze zawodowej energie wskazują na konkretny kierunek.",
        ],
        "advice": [
            "Skup się na tym, co możesz kontrolować: jakość pracy, komunikację i granice.",
            "Nie każda okazja jest Twoją okazją — wybieraj świadomie, nie z desperacji.",
            "Konsekwencja w małych krokach często wygrywa z wielkim, ale chaotycznym zrywem.",
        ],
    },
    "zdrowie": {
        "intro": [
            "W temacie zdrowia i samopoczucia karty zwracają uwagę na:",
            "Ciało i psychika są tu silnie powiązane.",
        ],
        "advice": [
            "Słuchaj sygnałów ciała wcześniej, niż staną się krzykiem.",
            "Regeneracja nie jest luksusem — to warunek dalszego działania.",
        ],
    },
    "decyzja": {
        "intro": [
            "Stoisz przed wyborem — karty nie zdejmują z Ciebie odpowiedzialności, ale rozjaśniają ścieżki.",
            "Przy decyzji, którą rozważasz, układ pokazuje napięcia i potencjały.",
        ],
        "advice": [
            "Zadaj sobie pytanie: której opcji boję się bardziej, a której naprawdę chcę?",
            "Dobra decyzja rzadko bywa w 100% wygodna — bywa za to zgodna z Twoimi wartościami.",
        ],
    },
    "czas": {
        "intro": [
            "Pytanie o czas w tarocie zawsze jest płynne — ważniejsze są warunki niż kalendarz.",
        ],
        "advice": [
            "Zamiast szukać daty, obserwuj, czy powtarza się ten sam wzorzec. Gdy się złamie — otwiera się nowe okno.",
        ],
    },
    "rozwoj": {
        "intro": [
            "W temacie rozwoju i wewnętrznej zmiany ten odczyt ma głębszy charakter.",
        ],
        "advice": [
            "Transformacja rzadko bywa komfortowa. Jeśli czujesz opór — sprawdź, czy chroni Cię, czy blokuje.",
        ],
    },
    "ogolny": {
        "intro": [
            "Odczyt układa się w spójną historię.",
            "Karty, które wypadły, budują konkretny obraz sytuacji.",
            "W tym układzie widać wyraźną linię napięć i możliwości.",
        ],
        "advice": [
            "Przyjmij wskazówki jako lustro, nie jako wyrok.",
            "Najwięcej zyskasz, jeśli zestawisz karty z tym, co już czujesz intuicyjnie.",
            "Działaj, ale nie zamykaj oczu na sygnały, które nie pasują do Twojego scenariusza.",
        ],
    },
}


def enrich_card_in_context(card: Dict, question: str, theme: str) -> str:
    """Buduje indywidualny opis karty w kontekście pozycji, orientacji i tematu pytania."""
    name = card["name_pl"]
    pos = card["position"]
    meaning = card["meaning"]
    rev = card["is_reversed"]
    guidance = card.get("position_guidance", "")

    orient_note = (
        "W pozycji odwróconej energia tej karty jest zahamowana, wypaczona albo domaga się integracji cienia."
        if rev else
        "W pozycji prostej karta działa w pełni — jej przesłanie jest bezpośrednie i dostępne."
    )

    # Warianty otwarcia zależne od pozycji
    pos_openers = {
        "Przeszłość": f"W przeszłości **{name}** wskazuje, że",
        "Teraźniejszość": f"Teraz **{name}** mówi, że",
        "Przyszłość": f"W nadchodzącym czasie **{name}** zapowiada, że",
        "Twoja odpowiedź": f"Bezpośrednia odpowiedź przez **{name}**:",
        "Sytuacja obecna": f"W centrum sprawy stoi **{name}** —",
        "Wyzwanie / przeszkoda": f"Główne wyzwanie, które niesie **{name}**:",
        "Ostateczny wynik": f"Jako możliwy rezultat **{name}** sugeruje, że",
        "Twoje podejście": f"Twoje obecne podejście, opisane przez **{name}**:",
        "Wpływ otoczenia": f"Z zewnątrz działa energia **{name}**:",
        "Nadzieje i obawy": f"Twoje nadzieje i lęki skupiają się wokół **{name}**:",
    }
    opener = pos_openers.get(pos, f"**{name}** w pozycji „{pos}”:")

    # Dopisek tematyczny
    theme_note = ""
    if theme == "milosc":
        theme_note = random.choice([
            " W relacjach ta energia często objawia się jako sposób, w jaki dajesz i przyjmujesz bliskość.",
            " W kontekście uczuć warto zobaczyć, czy ta karta opisuje Ciebie, drugą osobę, czy dynamikę między wami.",
        ])
    elif theme == "kariera":
        theme_note = random.choice([
            " W pracy może to dotyczyć zarówno konkretnego projektu, jak i Twojej postawy wobec odpowiedzialności.",
            " Zawodowo ta karta często wskazuje na styl działania, nie tylko na zewnętrzne okoliczności.",
        ])
    elif theme == "decyzja":
        theme_note = " Przy wyborze, przed którym stoisz, ta karta jest ważnym głosem — nie jedynym, ale znaczącym."

    body = f"{opener} {meaning.rstrip('.')}."
    extra = f" {orient_note}"
    if guidance:
        extra += f" {guidance}"
    extra += theme_note

    return body + extra


def get_card_combination_note(cards: List[Dict]) -> Optional[str]:
    """Dodaje unikalną uwagę, gdy w układzie pojawiają się charakterystyczne pary/energie."""
    names = {c["name_pl"] for c in cards}
    ids = {c["id"] for c in cards}
    major = [c for c in cards if c["arcana"] == "Wielkie"]
    reversed_cards = [c for c in cards if c["is_reversed"]]

    notes = []

    # Klasyczne napięcia
    if "Wieża" in names and "Wieża" in names:
        notes.append("Obecność Wieży ostrzega przed nagłym przełomem — czasem koniecznym, by powstało coś nowego.")
    if "Śmierć" in names:
        notes.append("Śmierć w układzie rzadko oznacza dosłowny koniec życia — częściej zamknięcie etapu i przestrzeń na odrodzenie.")
    if "Kochankowie" in names and any(c["name_pl"] in names for c in cards if "Miecz" in c.get("name_pl", "")):
        notes.append("Kochankowie obok energii mieczy sugerują, że wybór w relacji wymaga chłodniejszej głowy, nie tylko serca.")
    if "Diabeł" in names:
        notes.append("Diabeł wskazuje na przywiązanie — do osoby, nawyku, roli lub wygodnego kłamstwa. Uwolnienie zaczyna się od nazwania więzów.")
    if "Gwiazda" in names and "Księżyc" in names:
        notes.append("Gwiazda i Księżyc razem: nadzieja miesza się z niepewnością. Zaufaj intuicji, ale sprawdzaj fakty.")
    if "Słońce" in names and len(reversed_cards) >= 2:
        notes.append("Słońce w układzie z odwróconymi kartami: jasność jest dostępna, ale coś w Tobie lub w sytuacji jeszcze ją przesłania.")

    # Strukturalne
    if len(major) >= 3:
        notes.append(
            f"Aż {len(major)} Wielkich Arkanów w jednym odczycie — to nie jest zwykła codzienna sprawa. "
            "Tu grają większe siły: tożsamość, przeznaczenie, głęboka zmiana."
        )
    if len(reversed_cards) == len(cards) and len(cards) >= 2:
        notes.append(
            "Wszystkie karty odwrócone to silny sygnał: energia stoi, krąży w miejscu albo domaga się wewnętrznej pracy, zanim pójdzie na zewnątrz."
        )
    if len(reversed_cards) == 0 and len(cards) >= 3:
        notes.append(
            "Żadna karta nie wypadła odwrócona — przepływ jest stosunkowo czysty. To nie znaczy „łatwo”, ale znaczy „dostępne”."
        )

    # Kolory (suit)
    suits = [c.get("suit") for c in cards if c.get("suit")]
    if suits.count("Kielichy") >= 2:
        notes.append("Dominacja Kielichów: emocje, więzi i potrzeby serca są w tym odczycie na pierwszym planie.")
    if suits.count("Miecze") >= 2:
        notes.append("Dużo Mieczy: myśl, konflikt, decyzja i prawda — intelekt i komunikacja grają tu główną rolę.")
    if suits.count("Buławy") >= 2:
        notes.append("Buławy w większości: ogień działania, pasja, impuls i wola. Czas ruszyć, nie tylko planować.")
    if suits.count("Pentakle") >= 2:
        notes.append("Pentakle dominują: ciało, pieniądze, praca, stabilność i to, co namacalne. Stopy na ziemi.")

    if not notes:
        return None
    return random.choice(notes)


def get_synthesis(cards: List[Dict], question: str = "") -> str:
    theme = detect_theme(question)
    lens = THEME_LENSES.get(theme, THEME_LENSES["ogolny"])

    reversed_count = sum(1 for c in cards if c["is_reversed"])
    major_count = sum(1 for c in cards if c["arcana"] == "Wielkie")
    total = len(cards)

    parts = []

    # Intro zależne od tematu (losowe, by nie było schematycznie)
    parts.append(random.choice(lens["intro"]))

    # Opis dynamiki układu
    if reversed_count >= total * 0.6:
        parts.append(
            random.choice([
                "Dominuje energia odwrócona — coś jest zablokowane, opóźnione albo wymaga spojrzenia od drugiej strony.",
                "Większość kart stoi na głowie: to niekoniecznie „źle”, ale na pewno „inaczej, niż byś chciał”. Czas na korektę kursu.",
                "Układ pokazuje opór. Zanim pchniesz do przodu, warto zobaczyć, co dokładnie się opiera — i czy to naprawdę wróg.",
            ])
        )
    elif reversed_count == 0:
        parts.append(
            random.choice([
                "Wszystkie karty w pozycji prostej: energia jest dostępna i gotowa do użycia.",
                "Czysty przepływ — karty nie walczą ze sobą orientacją. To sprzyja klarownym decyzjom.",
            ])
        )
    else:
        parts.append(
            random.choice([
                "Układ jest mieszany: część energii płynie swobodnie, część wymaga uwagi i dopracowania.",
                "Nie wszystko jest ustawione idealnie — i właśnie w tym napięciu leży sedno odczytu.",
            ])
        )

    # Wielkie Arkana
    if major_count >= max(1, total * 0.5):
        parts.append(
            random.choice([
                "Silna obecność Wielkich Arkanów podnosi stawkę: tu nie chodzi tylko o detal, lecz o kierunek życiowy.",
                "Wielkie Arkana dominują — temat jest ważniejszy, niż może się wydawać na co dzień.",
            ])
        )
    elif major_count == 0 and total >= 3:
        parts.append(
            "Same Małe Arkana: sprawa dotyczy konkretów, rytmu dnia, relacji i działań, niekoniecznie wielkiego „przeznaczenia”."
        )

    # Unikalna nota o kombinacji
    combo = get_card_combination_note(cards)
    if combo:
        parts.append(combo)

    # Krótkie podsumowanie 1–2 kluczowych kart
    if total >= 1:
        key = cards[0] if total == 1 else random.choice(cards)
        orient = "odwrócona" if key["is_reversed"] else "prosta"
        parts.append(
            f"Szczególnie wybrzmiewa **{key['name_pl']}** ({key['position']}, {orient}): {key['meaning']}"
        )

    # Rada tematyczna
    parts.append(random.choice(lens["advice"]))

    return " ".join(parts)


def create_reading(spread_key: str, question: str = "") -> Dict[str, Any]:
    spread = SPREADS[spread_key]
    cards = draw_cards(len(spread["positions"]))
    theme = detect_theme(question)

    reading = {
        "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "timestamp": datetime.now().isoformat(),
        "spread": spread_key,
        "spread_name": spread["name"],
        "question": question.strip() or "Brak pytania",
        "theme": theme,
        "cards": []
    }

    for i, card in enumerate(cards):
        pos = spread["positions"][i]
        card_full = {
            **card,
            "position": pos,
            "position_guidance": POSITION_GUIDANCE.get(pos, "Ta pozycja wnosi ważny kontekst do odczytu."),
        }
        card_full["detailed"] = enrich_card_in_context(card_full, reading["question"], theme)
        reading["cards"].append(card_full)

    reading["synthesis"] = get_synthesis(reading["cards"], reading["question"])
    return reading


def answer_followup(question: str, cards: List[Dict], original_question: str = "") -> str:
    if not question.strip():
        return "Zadaj konkretne pytanie — im precyzyjniej, tym trafniejsza odpowiedź."

    theme = detect_theme(question)
    # Wybierz karty najbardziej „aktywne” — losowo 1-2, ale preferuj te z pozycji kluczowych
    priority_pos = {"Twoja odpowiedź", "Sytuacja obecna", "Teraźniejszość", "Ostateczny wynik", "Wyzwanie / przeszkoda"}
    priority = [c for c in cards if c["position"] in priority_pos]
    pool = priority if priority else cards
    selected = random.sample(pool, min(2, len(pool)))

    intro = random.choice([
        "W świetle kart, które już masz przed sobą:",
        "Odnosząc się do tego rozkładu:",
        "Karty odpowiadają na to dopytanie tak:",
        "Patrząc ponownie na układ pod kątem Twojego pytania:",
    ])

    lines = [intro, ""]
    for c in selected:
        orient = "odwrócona" if c["is_reversed"] else "prosta"
        lines.append(f"**{c['name_pl']}** ({c['position']}, {orient})")
        lines.append(c.get("detailed") or c["meaning"])
        lines.append("")

    lens = THEME_LENSES.get(theme, THEME_LENSES["ogolny"])
    lines.append(random.choice(lens["advice"]))
    lines.append("")
    lines.append("*" + random.choice([
        "Zatrzymaj się na chwilę z tą odpowiedzią — nie wszystko trzeba od razu „rozwiązać”.",
        "Jeśli coś w tej odpowiedzi mocno rezonuje lub mocno drażni — to zwykle ważny trop.",
        "Karty otwierają perspektywę; decyzja i odpowiedzialność zostają po Twojej stronie.",
    ]) + "*")

    return "\n".join(lines)
