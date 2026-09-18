import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
    /* Główne tło i typografia */
    .stApp {
        background: linear-gradient(180deg, #0d0b14 0%, #1a1025 50%, #0d0b14 100%);
        color: #e8e0d5;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #120e1c 0%, #1a1525 100%);
        border-right: 1px solid #3d2e5c;
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: #e8e0d5;
    }

    h1, h2, h3 {
        color: #c9a227 !important;
        font-family: 'Georgia', serif;
        letter-spacing: 1px;
    }

    .stButton > button {
        background: linear-gradient(135deg, #3d2e5c, #5a3d7a);
        color: #f5e8c7;
        border: 1px solid #c9a227;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        transition: all 0.25s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #5a3d7a, #7a4d9a);
        border-color: #e0c35a;
        box-shadow: 0 0 12px rgba(201, 162, 39, 0.4);
        color: #fff;
    }

    .card-box {
        background: rgba(26, 21, 37, 0.85);
        border: 1px solid #3d2e5c;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }

    /* ========== ANIMACJE KART ========== */

    @keyframes cardDeal {
        0% {
            opacity: 0;
            transform: translateY(-40px) scale(0.7) rotate(-8deg);
        }
        70% {
            opacity: 1;
            transform: translateY(6px) scale(1.03) rotate(2deg);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1) rotate(0deg);
        }
    }

    @keyframes cardFlipReveal {
        0% {
            transform: rotateY(90deg);
            opacity: 0.3;
        }
        100% {
            transform: rotateY(0deg);
            opacity: 1;
        }
    }

    @keyframes cardGlow {
        0%, 100% { box-shadow: 0 4px 18px rgba(201, 162, 39, 0.3); }
        50% { box-shadow: 0 6px 28px rgba(201, 162, 39, 0.6); }
    }

    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulseBack {
        0%, 100% { box-shadow: 0 0 12px rgba(120, 80, 180, 0.35); }
        50% { box-shadow: 0 0 22px rgba(180, 120, 255, 0.55); }
    }

    /* Karta – wspólne */
    .tarot-card, .tarot-card-back {
        border-radius: 12px;
        min-height: 210px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
        margin-bottom: 0.8rem;
        perspective: 1000px;
        transform-style: preserve-3d;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    /* REWERS (zakryta) */
    .tarot-card-back {
        background:
            radial-gradient(circle at 30% 30%, rgba(180, 120, 255, 0.15), transparent 50%),
            radial-gradient(circle at 70% 70%, rgba(201, 162, 39, 0.12), transparent 50%),
            linear-gradient(145deg, #1a1230, #2a1a45);
        border: 2px solid #6b4d9a;
        animation: cardDeal 0.6s ease-out both, pulseBack 2.5s ease-in-out infinite;
        cursor: default;
        position: relative;
        overflow: hidden;
    }

    .tarot-card-back::before {
        content: "✦";
        font-size: 2.8rem;
        color: #c9a227;
        opacity: 0.85;
        text-shadow: 0 0 20px rgba(201, 162, 39, 0.6);
    }

    .tarot-card-back::after {
        content: "";
        position: absolute;
        inset: 10px;
        border: 1px solid rgba(201, 162, 39, 0.35);
        border-radius: 8px;
        pointer-events: none;
    }

    .card-back-label {
        font-size: 0.75rem;
        color: #a89bb8;
        margin-top: 0.8rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* AWERS (odsłonięta) */
    .tarot-card {
        background: linear-gradient(145deg, #1f1830, #2a2040);
        border: 2px solid #c9a227;
        padding: 1.1rem 0.9rem;
        animation: cardFlipReveal 0.65s ease-out both, cardGlow 3s ease-in-out 0.65s infinite;
    }

    .tarot-card.reversed {
        border-color: #9b4d6e;
        background: linear-gradient(145deg, #2a1830, #3a2040);
    }

    .tarot-card:hover, .tarot-card-back:hover {
        transform: translateY(-6px) scale(1.02);
    }

    /* Stagger delays */
    .delay-0 { animation-delay: 0.05s; }
    .delay-1 { animation-delay: 0.2s; }
    .delay-2 { animation-delay: 0.35s; }
    .delay-3 { animation-delay: 0.5s; }
    .delay-4 { animation-delay: 0.65s; }
    .delay-5 { animation-delay: 0.8s; }
    .delay-6 { animation-delay: 0.95s; }
    .delay-7 { animation-delay: 1.1s; }
    .delay-8 { animation-delay: 1.25s; }
    .delay-9 { animation-delay: 1.4s; }

    .card-position {
        font-size: 0.78rem;
        color: #a89bb8;
        margin-bottom: 0.45rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        animation: fadeSlideUp 0.45s ease-out both;
    }

    .card-name {
        font-size: 1.15rem;
        font-weight: 700;
        color: #c9a227;
        margin-bottom: 0.45rem;
        animation: fadeSlideUp 0.45s ease-out 0.12s both;
    }

    .card-meaning {
        font-size: 0.88rem;
        color: #d4c8b8;
        line-height: 1.45;
        animation: fadeSlideUp 0.45s ease-out 0.25s both;
    }

    /* Horoskop */
    .horoscope-section {
        background: rgba(30, 22, 45, 0.7);
        border-left: 4px solid #c9a227;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        border-radius: 0 8px 8px 0;
        animation: fadeSlideUp 0.5s ease-out both;
    }

    .horoscope-section h4 {
        color: #c9a227 !important;
        margin-bottom: 0.4rem;
        font-size: 1.05rem;
    }

    .stSelectbox label, .stTextInput label, .stTextArea label {
        color: #c9a227 !important;
        font-weight: 600;
    }

    div[data-testid="stMetric"] {
        background: rgba(26, 21, 37, 0.6);
        border: 1px solid #3d2e5c;
        border-radius: 10px;
        padding: 0.8rem;
    }

    hr {
        border-color: #3d2e5c;
        margin: 1.5rem 0;
    }

    .footer {
        text-align: center;
        color: #7a6e8a;
        font-size: 0.85rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #2a2035;
    }
    </style>
    """, unsafe_allow_html=True)


def card_back_html(position: str, delay_index: int = 0) -> str:
    delay_class = f"delay-{min(delay_index, 9)}"
    return f"""
    <div class="tarot-card-back {delay_class}">
        <div class="card-back-label">{position}</div>
    </div>
    """


def card_html(name: str, position: str, meaning: str, reversed: bool = False, delay_index: int = 0) -> str:
    rev_class = "reversed" if reversed else ""
    rev_label = " (odwrócona)" if reversed else ""
    delay_class = f"delay-{min(delay_index, 9)}"
    return f"""
    <div class="tarot-card {rev_class} {delay_class}">
        <div class="card-position">{position}</div>
        <div class="card-name">{name}{rev_label}</div>
        <div class="card-meaning">{meaning}</div>
    </div>
    """


def horoscope_section(title: str, text: str) -> str:
    return f"""
    <div class="horoscope-section">
        <h4>{title}</h4>
        <p style="margin:0; color:#d4c8b8; line-height:1.5;">{text}</p>
    </div>
    """
