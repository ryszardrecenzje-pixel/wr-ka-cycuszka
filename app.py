import sys
from pathlib import Path

ROOT = Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from utils.style import inject_custom_css

st.set_page_config(
    page_title="Wróżka",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_css()

if "tarot_history" not in st.session_state:
    st.session_state.tarot_history = []

st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem 0;">
    <h1 style="font-size: 3rem; margin-bottom: 0.3rem;">🔮 Wróżka</h1>
    <p style="font-size: 1.25rem; color: #a89bb8; margin-bottom: 0.5rem;">
        Twoja cyfrowa wróżka online
    </p>
    <p style="color: #7a6e8a; font-style: italic;">
        „Karty już czekają… co chcesz wiedzieć?”
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div class="card-box" style="text-align:center;">
        <h3>🃏 Tarot</h3>
        <p style="color:#d4c8b8;">
            Wybierz układ, zadaj pytanie i otrzymaj interpretację kart.
            Dostępne układy: 1 karta, 3 karty oraz pełny Krzyż Celtycki.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Przejdź do Tarota →", use_container_width=True, type="primary", key="btn_tarot"):
        try:
            st.switch_page("pages/1_Tarot.py")
        except Exception:
            st.info("👉 Otwórz **Tarot** z menu po lewej stronie (sidebar).")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card-box" style="text-align:center;">
        <h3>♈ Horoskopy</h3>
        <p style="color:#d4c8b8;">
            Sprawdź energię dnia, tygodnia lub miesiąca dla swojego znaku zodiaku.
            Miłość, kariera, zdrowie i rada – wszystko w jednym miejscu.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Przejdź do Horoskopów →", use_container_width=True, type="primary", key="btn_horoscope"):
        try:
            st.switch_page("pages/2_Horoskopy.py")
        except Exception:
            st.info("👉 Otwórz **Horoskopy** z menu po lewej stronie (sidebar).")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card-box" style="text-align:center;">
        <h3>📜 Historia odczytów</h3>
        <p style="color:#d4c8b8;">
            Wszystkie Twoje odczyty tarota są zapisywane w sesji.
            Możesz do nich wrócić i wyeksportować do PDF w module Tarot.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-box" style="text-align:center; margin-top: 1rem;">
        <p style="color:#a89bb8; margin:0;">
            💡 <b>Wskazówka:</b> Nawigacja działa też przez lewy panel (sidebar):
            <br><b>app</b> → <b>Tarot</b> → <b>Horoskopy</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<div class="footer">
    Stworzone z ❤️ i odrobiną magii • Streamlit + Python<br>
    Wersja rozszerzona • Gotowa do wdrożenia na GitHub + Streamlit Cloud
</div>
""", unsafe_allow_html=True)
