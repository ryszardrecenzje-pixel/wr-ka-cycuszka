"""Interpretacje tarota przez Groq (darmowy tier)."""
from __future__ import annotations

import streamlit as st
from typing import Any, Dict, Optional


def _get_groq_client():
    api_key = None
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        pass
    if not api_key:
        return None
    try:
        from groq import Groq
        return Groq(api_key=api_key)
    except Exception:
        return None


def is_ai_available() -> bool:
    return _get_groq_client() is not None


def _build_cards_text(cards: list) -> str:
    lines = []
    for c in cards:
        orient = "odwrócona" if c.get("is_reversed") else "prosta"
        lines.append(
            f"- {c.get('position', '?')}: {c.get('name_pl', c.get('name', '?'))} "
            f"({orient}) — {c.get('meaning', '')}"
        )
    return "\n".join(lines)


def _build_prompt(reading: Dict[str, Any], followup: Optional[str] = None) -> str:
    cards_txt = _build_cards_text(reading.get("cards", []))
    question = reading.get("question") or "Brak konkretnego pytania"
    spread = reading.get("spread_name", "układ tarota")

    base = f"""Jesteś doświadczoną, ciepłą i mądrą wróżką tarota. Piszesz wyłącznie po polsku.
Styl: naturalny, indywidualny, bez kiczu, bez straszenia, bez ogólników „na jedno kopyto”.

Pytanie użytkownika: {question}
Układ: {spread}

Karty, które wypadły:
{cards_txt}

Zasady odpowiedzi:
- Odnos się KONKRETNIE do tych kart, ich pozycji i orientacji (prosta/odwrócona)
- Łącz karty w spójną historię, nie wymieniaj ich tylko po kolei
- Bądź osobista — pisz tak, jakbyś mówiła do jednej osoby
- Unikaj frazesów typu „ufaj wszechświatowi” bez pokrycia w kartach
- Na końcu podaj 1–2 konkretne, praktyczne wskazówki
- Długość: ok. 180–280 słów
"""
    if followup and followup.strip():
        base += f"""
Dodatkowe pytanie użytkownika: {followup.strip()}

Zadanie: odpowiedz głównie na to dodatkowe pytanie, ale zawsze w kontekście powyższych kart.
"""
    else:
        base += """
Zadanie: napisz syntezę całego odczytu — co ten układ mówi o sytuacji użytkownika.
"""
    return base


def generate_interpretation(
    reading: Dict[str, Any],
    followup: Optional[str] = None,
    model: str = "llama-3.1-8b-instant",
) -> Optional[str]:
    """
    Generuje interpretację przez Groq.
    Zwraca tekst albo None (brak klucza / błąd) — wtedy użyj fallbacku lokalnego.
    """
    client = _get_groq_client()
    if client is None:
        return None

    prompt = _build_prompt(reading, followup)

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Jesteś mądrą, empatyczną wróżką tarota. "
                        "Odpowiadasz po polsku, konkretnie i z szacunkiem do użytkownika."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.85,
            max_tokens=700,
        )
        text = resp.choices[0].message.content
        if text:
            return text.strip()
    except Exception as e:
        # Nie crashuj apki — po prostu wróć do lokalnej syntezy
        st.session_state["_ai_last_error"] = str(e)
        return None

    return None
