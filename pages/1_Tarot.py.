import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from utils.style import inject_custom_css, card_html, card_back_html
from utils.tarot_logic import SPREADS, create_reading, get_synthesis, answer_followup
from utils.pdf_export import create_tarot_pdf

st.set_page_config(page_title="Tarot • Wróżka", page_icon="🃏", layout="wide")
inject_custom_css()

if "tarot_history" not in st.session_state:
    st.session_state.tarot_history = []
if "cards_revealed" not in st.session_state:
    st.session_state.cards_revealed = False
if "followup_answers" not in st.session_state:
    st.session_state.followup_answers = []

st.title("🃏 Tarot")
st.caption("Wybierz układ, zadaj pytanie i pozwól kartom mówić. Po odsłonięciu możesz dopytać o szczegóły.")

# ---------- Ustawienia ----------
col_left, col_right = st.columns([1, 1])

with col_left:
    spread_key = st.selectbox(
        "Wybierz układ",
        options=list(SPREADS.keys()),
        format_func=lambda k: SPREADS[k]["name"],
        help="Różne układy dają różny poziom szczegółowości."
    )
    st.info(SPREADS[spread_key]["description"])

with col_right:
    question = st.text_area(
        "Twoje pytanie (opcjonalnie, ale bardzo pomaga)",
        placeholder="Np. Co powinienem wiedzieć o mojej sytuacji zawodowej? Jak potoczy się ta relacja?",
        height=100
    )
    allow_reversed = st.checkbox("Uwzględniaj karty odwrócone", value=True)
    st.caption("Karty odwrócone często wskazują na blokady, opóźnienia lub odwrócenie energii karty.")

st.markdown("---")

# ---------- Losowanie ----------
if st.button("✨ Rozłóż karty", use_container_width=True, type="primary"):
    with st.spinner("Tasuję talię i skupiam intencję..."):
        reading = create_reading(spread_key, question)
        reading["synthesis"] = get_synthesis(reading["cards"])
        if not allow_reversed:
            for c in reading["cards"]:
                c["is_reversed"] = False
                c["meaning"] = c["upright"]

        st.session_state.current_reading = reading
        st.session_state.cards_revealed = False
        st.session_state.followup_answers = []
        st.session_state.tarot_history.insert(0, reading)
        st.session_state.tarot_history = st.session_state.tarot_history[:20]

# ---------- Odczyt ----------
if "current_reading" in st.session_state:
    reading = st.session_state.current_reading
    revealed = st.session_state.get("cards_revealed", False)

    st.markdown(f"### Układ: **{reading['spread_name']}**")
    if reading["question"] != "Brak pytania":
        st.markdown(f"**Twoje pytanie:** *{reading['question']}*")
    else:
        st.markdown("*Nie zadano konkretnego pytania — odczyt ma charakter ogólny.*")

    st.markdown("")

    cards = reading["cards"]
    n = len(cards)

    if n == 1:
        cols = st.columns(1)
    elif n <= 3:
        cols = st.columns(n)
    elif n == 10:
        row1 = st.columns(4)
        row2 = st.columns(3)
        row3 = st.columns(3)
        cols = list(row1) + list(row2) + list(row3)
    else:
        cols = st.columns(min(n, 5))

    for i, card in enumerate(cards):
        with cols[i % len(cols)]:
            if not revealed:
                html = card_back_html(position=card["position"], delay_index=i)
            else:
                html = card_html(
                    name=card["name_pl"],
                    position=card["position"],
                    meaning=card["meaning"],
                    reversed=card["is_reversed"],
                    delay_index=i
                )
            st.markdown(html, unsafe_allow_html=True)

    if not revealed:
        st.markdown("")
        if st.button("🔮 Odsłoń karty", use_container_width=True, type="primary"):
            st.session_state.cards_revealed = True
            st.rerun()
        st.caption("Karty leżą zakryte. Skup się na pytaniu, a potem je odsłoń.")
    else:
        # --- Szczegółowe wyjaśnienia pozycji ---
        st.markdown("---")
        st.markdown("### 📖 Szczegółowe wyjaśnienie kart")

        for card in cards:
            with st.expander(f"{'↺ ' if card['is_reversed'] else ''}{card['name_pl']} — {card['position']}", expanded=(n <= 3)):
                orient = "odwrócona" if card["is_reversed"] else "prosta"
                st.markdown(f"**Orientacja:** {orient}")
                st.markdown(f"**Znaczenie w tej pozycji:** {card['meaning']}")
                st.markdown(f"**Co mówi pozycja „{card['position']}”?**  \n{card.get('position_guidance', '')}")
                if card["arcana"] == "Wielkie":
                    st.markdown("*To Wielkie Arkanum — energia o większej wadze, często związana z ważnymi życiowymi tematami.*")
                elif card.get("suit"):
                    st.markdown(f"*Małe Arkanum, kolor: **{card['suit']}**.*")

        # --- Synteza ---
        st.markdown("---")
        st.markdown("### 📜 Synteza odczytu")
        st.markdown(f"""
        <div class="card-box">
            <p style="color:#d4c8b8; line-height:1.7; margin:0;">{reading['synthesis']}</p>
        </div>
        """, unsafe_allow_html=True)

        # --- Pytania dodatkowe ---
        st.markdown("---")
        st.markdown("### 💬 Dopytaj karty")
        st.markdown(
            "Możesz zadać **dodatkowe pytanie** związane z tym odczytem. "
            "Odpowiedź powstanie na podstawie kart, które już wypadły."
        )

        followup_q = st.text_input(
            "Twoje dodatkowe pytanie",
            placeholder="Np. Jak to wpływa na moją relację? Co powinienem zrobić w pracy? Kiedy spodziewać się zmian?",
            key="followup_input"
        )

        if st.button("✨ Uzyskaj odpowiedź", key="btn_followup"):
            if followup_q.strip():
                ans = answer_followup(followup_q, cards)
                st.session_state.followup_answers.insert(0, {
                    "question": followup_q.strip(),
                    "answer": ans
                })
            else:
                st.warning("Wpisz pytanie, zanim poprosisz o odpowiedź.")

        if st.session_state.followup_answers:
            st.markdown("#### Poprzednie dopytania")
            for i, fa in enumerate(st.session_state.followup_answers):
                with st.expander(f"Q: {fa['question'][:60]}{'…' if len(fa['question']) > 60 else ''}", expanded=(i == 0)):
                    st.markdown(f"**Pytanie:** {fa['question']}")
                    st.markdown(fa["answer"])

        # PDF
        st.markdown("")
        pdf_bytes = create_tarot_pdf(reading)
        st.download_button(
            label="📄 Pobierz odczyt jako PDF",
            data=pdf_bytes,
            file_name=f"tarot_{reading['id']}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# ---------- Historia ----------
st.markdown("---")
st.subheader("📜 Historia odczytów (ta sesja)")

if not st.session_state.tarot_history:
    st.info("Brak zapisanych odczytów. Rozłóż pierwsze karty!")
else:
    for idx, past in enumerate(st.session_state.tarot_history):
        with st.expander(f"{past['spread_name']} • {past['timestamp'][:16].replace('T', ' ')} • {past['question'][:40]}..."):
            st.write(f"**Pytanie:** {past['question']}")
            for c in past["cards"]:
                rev = " ↺" if c["is_reversed"] else ""
                st.markdown(f"- **{c['position']}**: {c['name_pl']}{rev} — {c['meaning']}")
            if past.get("synthesis"):
                st.markdown(f"*Synteza:* {past['synthesis']}")
            pdf_bytes = create_tarot_pdf(past)
            st.download_button(
                label="📄 PDF",
                data=pdf_bytes,
                file_name=f"tarot_{past['id']}.pdf",
                mime="application/pdf",
                key=f"pdf_{idx}"
            )
