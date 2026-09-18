from fpdf import FPDF
from datetime import datetime
from typing import Dict, Any
import io
import re

def sanitize_text(text: str) -> str:
    """Zamienia polskie znaki na ASCII, żeby fpdf2 nie wywalał błędu."""
    if not text:
        return ""
    replacements = {
        "ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n",
        "ó": "o", "ś": "s", "ź": "z", "ż": "z",
        "Ą": "A", "Ć": "C", "Ę": "E", "Ł": "L", "Ń": "N",
        "Ó": "O", "Ś": "S", "Ź": "Z", "Ż": "Z",
        "–": "-", "—": "-", "„": '"', "”": '"', "«": '"', "»": '"',
        "…": "...",
    }
    for pl, ascii_char in replacements.items():
        text = text.replace(pl, ascii_char)
    # Usuń pozostałe znaki spoza Latin-1
    text = text.encode("latin-1", errors="replace").decode("latin-1")
    return text


class MysticalPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(150, 100, 30)
        self.cell(0, 10, "Wrozka - Odczyt Tarota", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 110, 130)
        self.cell(
            0, 10,
            f"Wygenerowano: {datetime.now().strftime('%d.%m.%Y %H:%M')}  |  strona {self.page_no()}",
            align="C"
        )


def create_tarot_pdf(reading: Dict[str, Any]) -> bytes:
    pdf = MysticalPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    # Pytanie
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(50, 40, 70)
    pdf.cell(0, 8, "Pytanie:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    question = sanitize_text(reading.get("question", "Brak pytania"))
    pdf.multi_cell(0, 7, question)
    pdf.ln(4)

    # Uklad
    pdf.set_font("Helvetica", "B", 12)
    spread_name = sanitize_text(reading.get("spread_name", ""))
    pdf.cell(0, 8, f"Uklad: {spread_name}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # Karty
    for card in reading.get("cards", []):
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(150, 100, 30)
        pos = sanitize_text(card.get("position", ""))
        name = sanitize_text(card.get("name_pl", card.get("name", "")))
        rev = " (odwrocona)" if card.get("is_reversed") else ""
        pdf.cell(0, 7, f"{pos}: {name}{rev}", new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(40, 30, 50)
        meaning = sanitize_text(card.get("meaning", ""))
        pdf.multi_cell(0, 6, meaning)
        pdf.ln(4)

    # Synteza
    if reading.get("synthesis"):
        pdf.ln(4)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(150, 100, 30)
        pdf.cell(0, 7, "Synteza odczytu:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(40, 30, 50)
        synthesis = sanitize_text(reading["synthesis"])
        pdf.multi_cell(0, 6, synthesis)

    buffer = io.BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()
