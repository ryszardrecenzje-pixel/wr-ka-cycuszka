import sys
from pathlib import Path

# Naprawa ścieżki dla Streamlit Cloud
ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from utils.style import inject_custom_css, horoscope_section
from utils.horoscope_logic import ZODIAC_SIGNS, generate_horoscope, get_period_label

st.set_page_config(page_title="Horoskopy • Wróżka", page_icon="♈", layout="wide")
inject_custom_css()

st.title("♈ Horoskopy")
st.caption("Wybierz swój znak i sprawdź energię dnia, tygodnia lub miesiąca.")

# ---------- Wybór znaku ----------
st.markdown("### Wybierz znak zodiaku")

# Siatka znaków
sign_keys = list(ZODIAC_SIGNS.keys())
cols = st.columns(6)

selected_sign = None
for i, key in enumerate(sign_keys):
    info = ZODIAC_SIGNS[key]
    with cols[i % 6]:
        if st.button(f"{info['emoji']} {info['name']}", key=f"sign_{key}", use_container_width=True):
            st.session_state.selected_sign = key

if "selected_sign" not in st.session_state:
    st.session_state.selected_sign = "skorpion"  # domyślny

selected_sign = st.session_state.selected_sign
sign_info = ZODIAC_SIGNS[selected_sign]

st.markdown(f"""
<div class="card-box" style="text-align:center; margin-top:1rem;">
    <h2 style="margin:0;">{sign_info['emoji']} {sign_info['name']}</h2>
    <p style="color:#a89bb8; margin:0.3rem 0 0 0;">{sign_info['dates']} • Żywioł: {sign_info['element']}</p>
</div>
""", unsafe_allow_html=True)

# ---------- Wybór okresu ----------
period = st.radio(
    "Okres",
    options=["dzienny", "tygodniowy", "miesieczny"],
    format_func=lambda p: get_period_label(p),
    horizontal=True
)

st.markdown("---")

# ---------- Generowanie ----------
if st.button("✨ Pokaż horoskop", use_container_width=True, type="primary"):
    with st.spinner("Odczytuję gwiazdy..."):
        result = generate_horoscope(selected_sign, period)
        st.session_state.current_horoscope = result

# ---------- Wyświetlanie ----------
if "current_horoscope" in st.session_state:
    h = st.session_state.current_horoscope

    if "error" in h:
        st.error(h["error"])
    else:
        st.markdown(f"### {h['emoji']} {get_period_label(h['period'])} • {h['date']}")

        st.markdown(horoscope_section("✨ Energia ogólna", h["general"]), unsafe_allow_html=True)
        st.markdown(horoscope_section("💖 Miłość i relacje", h["love"]), unsafe_allow_html=True)
        st.markdown(horoscope_section("💼 Kariera i finanse", h["career"]), unsafe_allow_html=True)
        st.markdown(horoscope_section("🌿 Zdrowie i samopoczucie", h["health"]), unsafe_allow_html=True)
        st.markdown(horoscope_section("🗝️ Rada na ten okres", h["advice"]), unsafe_allow_html=True)

        # Szczęśliwe elementy
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Szczęśliwa liczba", h["lucky_number"])
        with c2:
            st.metric("Szczęśliwy kolor", h["lucky_color"])

st.markdown("---")
st.caption("Horoskopy są generowane lokalnie na podstawie szablonów. Wersja zaawansowana może dodać generowanie AI.")
