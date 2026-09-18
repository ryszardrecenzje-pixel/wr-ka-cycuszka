# 🔮 Wróżka – Streamlit App

Aplikacja typu wróżka z dwoma głównymi modułami:

- **Tarot** – układy 1 karta / 3 karty / Krzyż Celtycki + historia + eksport PDF
- **Horoskopy** – dzienny / tygodniowy / miesięczny dla wszystkich 12 znaków zodiaku

## Funkcje (wersja rozszerzona)

- Ciemny, mistyczny motyw (fiolet + złoto)
- Pełna talia 78 kart tarota (Wielkie + Małe Arkana) z znaczeniami upright/reversed
- Trzy gotowe układy tarota
- Historia odczytów w sesji (do 20 ostatnich)
- Eksport odczytu tarota do PDF
- Horoskopy z losowanymi wariantami tekstów
- Szczęśliwa liczba i kolor
- Responsywny layout

## Uruchomienie lokalne

```bash
# 1. Sklonuj repo
git clone <twoje-repo>
cd wrozka-streamlit

# 2. Środowisko wirtualne (opcjonalnie)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Zainstaluj zależności
pip install -r requirements.txt

# 4. Uruchom
streamlit run app.py
```

## Wdrożenie na Streamlit Cloud

1. Wrzuć projekt na GitHub
2. Wejdź na [share.streamlit.io](https://share.streamlit.io)
3. Połącz repozytorium
4. Main file path: `app.py`
5. Deploy

## Struktura projektu

```
wrozka-streamlit/
├── app.py                     # Strona główna
├── pages/
│   ├── 1_🃏_Tarot.py          # Moduł Tarot
│   └── 2_♈_Horoskopy.py      # Moduł Horoskopy
├── data/
│   ├── tarot_cards.json       # 78 kart
│   └── horoscopes/            # 12 plików JSON znaków
├── utils/
│   ├── style.py               # CSS + helpery HTML
│   ├── tarot_logic.py         # Logika tarota
│   ├── horoscope_logic.py     # Logika horoskopów
│   └── pdf_export.py          # Generowanie PDF
├── .streamlit/
│   └── config.toml            # Motyw
├── requirements.txt
└── README.md
```

## Co dalej? (wersja zaawansowana)

- Generowanie interpretacji przez LLM (OpenAI / Grok / lokalny model)
- Zapisywanie historii na stałe (SQLite / plik)
- Upload własnych znaczeń kart
- Udostępnianie odczytu linkiem
- Animacje odwracania kart
- Więcej układów tarota

## Licencja

MIT – używaj swobodnie.


## Interpretacja AI (Groq) — darmowa

1. Załóż konto na https://console.groq.com i utwórz API key
2. Na Streamlit Cloud: **App settings → Secrets** dodaj:

```toml
GROQ_API_KEY = "gsk_..."
```

3. W aplikacji włącz przełącznik **Interpretacja AI (Groq)**

Bez klucza działa lokalny silnik interpretacji (fallback).

Model domyślny: `llama-3.1-8b-instant` (szybki, darmowy tier).
