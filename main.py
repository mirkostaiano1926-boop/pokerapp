import streamlit as st
import random
import pandas as pd

# ==========================================
# 1. SETUP TERMINALE DI COMANDO
# ==========================================
st.set_page_config(page_title="WAR MACHINE: JUDGMENT DAY", layout="wide", page_icon="💀")

# CSS PROFESSIONALE (Look GTO Wizard / High-End Trading)
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #00ffcc; }
    .gto-grid { display: grid; grid-template-columns: repeat(13, 1fr); gap: 2px; width: 100%; }
    .gto-cell { aspect-ratio: 1/1; display: flex; align-items: center; justify-content: center; 
                border-radius: 2px; font-size: 10px; font-weight: bold; color: white; transition: 0.2s; }
    .pair { background: #4a0000; border: 1px solid #ff0000; }
    .suited { background: #002244; border: 1px solid #0077ff; }
    .offsuit { background: #1a1a1a; border: 1px solid #333; }
    .gto-open { background: #00ff88 !important; color: black !important; box-shadow: 0 0 15px #00ff88; }
    .gto-3bet { background: #ff00ff !important; box-shadow: 0 0 15px #ff00ff; }
    .gto-fold { opacity: 0.1; filter: blur(1px); }
    .stMetric { border: 1px solid #333; background: #111; padding: 15px; border-radius: 10px; }
    .ai-card { background: #0e1117; border-left: 5px solid #00ffcc; padding: 20px; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MOTORE STRATEGICO CORE
# ==========================================
RANKS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
RANGES = {
    "UTG_OPEN": ["AA","KK","QQ","JJ","TT","99","88","77","AKs","AQs","AJs","ATs","AKo","AQo","KQs"],
    "BTN_OPEN": ["22+","A2s+","K2s+","Q5s+","J7s+","T7s+","97s+","86s+","A2o+","K8o+","Q9o+","J9o+"],
    "3BET_RANGE": ["AA","KK","QQ","JJ","AKs","AQs","A5s","A4s","KQs","AKo"],
    "DEFENSE": ["TT","99","88","77","AQs","AJs","KQs","QJs","JTs","T9s"]
}

if 'score' not in st.session_state: st.session_state.score = 0
if 'opponents' not in st.session_state: st.session_state.opponents = []

# ==========================================
# 3. INTERFACCIA A 3 COLONNE (IL MOSTRO)
# ==========================================
st.title("💀 POKER WAR MACHINE: JUDGMENT DAY")
st.write("---")

col_left, col_mid, col_right = st.columns([1.2, 1.5, 1.2])

# ------------------------------------------
# COLONNA SINISTRA: TACTICAL WAR ROOM
# ------------------------------------------
with col_left:
    st.header("🚀 Tactical Room")
    with st.container():
        st.subheader("Decision Engine")
        pot = st.number_input("Piatto Totale", value=1000, step=100)
        call = st.number_input("Costo Call", value=500, step=50)
        outs = st.slider("I tuoi Outs", 1, 21, 9)
        fase = st.selectbox("Fase", ["Flop (x4)", "Turn (x2)"])
        
        # Calcoli Avanzati
        eq = outs * 4 if "Flop" in fase else outs * 2
        odds = (call / (pot + call)) * 100
        diff = eq - odds
        
        st.metric("Equity REALE", f"{eq}%", delta=f"{diff:.1f}%")
        
        if eq >= odds:
            st.success("✅ CALL PROFITTEVOLE")
            st.caption(f"Gu
