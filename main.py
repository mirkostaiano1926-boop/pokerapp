import streamlit as st
import random

st.set_page_config(page_title="WAR MACHINE OMEGA", layout="wide", page_icon="🔱")

st.markdown("""
<style>
    .stApp { background-color: #020202; color: #00ffcc; }
    .gto-cell { display: flex; align-items: center; justify-content: center; height: 32px; width: 32px; border-radius: 3px; font-size: 8px; font-weight: bold; color: white; margin: 1px; }
    .pair { background: #ff1744; }
    .suited { background: #2979ff; }
    .offsuit { background: #263238; border: 1px solid #37474f; }
    .gto-open { background: #00e676 !important; color: black !important; box-shadow: 0 0 10px #00e676; border: 1px solid white !important; }
    .gto-fold { opacity: 0.15; filter: grayscale(100%); }
    .stMetric { border: 1px solid #00ffcc; border-radius: 12px; background: rgba(0,255,204,0.05); padding: 10px; }
</style>
""", unsafe_allow_html=True)

RANGES = {
    "UTG": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "AKs", "AQs", "AJs", "ATs", "AKo", "AQo", "KQs"],
    "HJ": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "AKs", "AQs", "AJs", "ATs", "A9s", "AKo", "AQo", "KQs", "KJs", "QJs", "JTs"],
    "BTN": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22", "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s", "AKo", "AQo", "AJo", "ATo", "A9o", "A8o", "A7o", "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "KJo", "KTo", "QJs", "QTs", "Q9s", "JTs", "J9s", "T9s", "98s", "87s", "76s"]
}
RANKS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

st.sidebar.title("🔱 OMEGA V7.1")
menu = st.sidebar.selectbox("MENU:", ["📊 GTO MATRIX", "🚀 WAR ROOM", "🎓 TRAINING", "⏳ MASTER"])

if menu == "📊 GTO MATRIX":
    st.title("📊 Matrix GTO")
    pos = st.selectbox("Posizione:", ["Nessuno", "UTG", "HJ", "BTN"])
    for r_idx, r in enumerate(RANKS):
        cols = st.columns(13)
        for c_idx, c in enumerate(RANKS):
            if r_idx == c_idx: hand, style = r+c, "pair"
            elif c_idx > r_idx: hand, style = r+c+"s", "suited"
            else: hand, style = c+r+"o", "offsuit"
            is_active = pos != "Nessuno" and hand in RANGES.get(pos, [])
            cl = f"gto-cell {style}" + (" gto-open" if is_active else " gto-fold" if pos != "Nessuno" else "")
            cols[c_idx].markdown(f'<div class="{cl}">{hand}</div>', unsafe_allow_html=True)

elif menu == "🚀 WAR ROOM":
    st.title("🚀 War Room")
    pot = st.number_input("Piatto", value=1000)
    call = st.number_input("Costo", value=500)
    eq = st.slider("Tua Equity %", 0, 100, 35)
    odds = (call / (pot + call)) * 100
    st.metric("Pot Odds richieste", f"{odds:.1f}%")
    if eq >= odds: st.success("✅ CHIAMA")
    else: st.error("❌ PASSA")

elif menu == "🎓 TRAINING":
    st.title("🎓 Arena")
    if st.button("PROSSIMA MANO"): st.session_state.th = random.choice(["AA", "72o", "KJs", "44"])
    if 'th' in st.session_state: st.subheader(f"Hai {st.session_state.th}. Cosa fai?")

elif menu == "⏳ MASTER":
    st.title("⏳ Survival")
    stk = st.number_input("Stack", value=5000)
    bb = st.number_input("BB", value=400)
    st.metric("M-Ratio", f"{stk/(bb*1.5):.1f}")
