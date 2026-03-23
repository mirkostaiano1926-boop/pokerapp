import streamlit as st
import random
import pandas as pd

# ==========================================
# 1. SETUP TERMINALE DI COMANDO (PC WIDE)
# ==========================================
st.set_page_config(page_title="WAR MACHINE: JUDGMENT DAY", layout="wide", page_icon="💀")

# CSS PROFESSIONALE PER PC (GTO WIZARD STYLE)
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #00ffcc; }
    .gto-grid { display: grid; grid-template-columns: repeat(13, 1fr); gap: 2px; width: 100%; max-width: 550px; margin: 0 auto; }
    .gto-cell { aspect-ratio: 1/1; display: flex; align-items: center; justify-content: center; 
                border-radius: 2px; font-size: 10px; font-weight: bold; color: white; transition: 0.2s; }
    .pair { background: #4a0000; border: 1px solid #ff0000; }
    .suited { background: #002244; border: 1px solid #0077ff; }
    .offsuit { background: #1a1a1a; border: 1px solid #333; }
    .gto-open { background: #00ff88 !important; color: black !important; box-shadow: 0 0 15px #00ff88; border: 1px solid white !important; }
    .gto-3bet { background: #ff00ff !important; box-shadow: 0 0 15px #ff00ff; border: 1px solid white !important; }
    .gto-fold { opacity: 0.1; filter: grayscale(100%); }
    .stMetric { border: 1px solid #333; background: #111; padding: 15px; border-radius: 10px; }
    .ai-card { background: #0e1117; border-left: 5px solid #00ffcc; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MOTORE STRATEGICO CORE
# ==========================================
RANKS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

RANGES = {
    "UTG_OPEN": ["AA","KK","QQ","JJ","TT","99","88","77","AKs","AQs","AJs","ATs","AKo","AQo","KQs"],
    "BTN_OPEN": ["AA","KK","QQ","JJ","TT","99","88","77","66","55","44","33","22",
                 "AKs","AQs","AJs","ATs","A9s","A8s","A7s","A6s","A5s","A4s","A3s","A2s",
                 "KQs","KJs","KTs","K9s","K8s","K7s","K6s","QJs","QTs","Q9s","JTs","J9s","T9s","98s","87s",
                 "AKo","AQo","AJo","ATo","A9o","A8o","KQs","KJo","KTo","QJo","QTo","JTo"],
    "3BET": ["AA","KK","QQ","AKs","A5s","A4s","KQs","AKo"],
    "DEFENSE": ["TT","99","88","77","AQs","AJs","KQs","QJs","JTs","98s"]
}

if 'opponents' not in st.session_state: st.session_state.opponents = []

# ==========================================
# 3. INTERFACCIA A 3 COLONNE (IL MOSTRO)
# ==========================================
st.title("💀 POKER WAR MACHINE: JUDGMENT DAY")
st.write("---")

col_left, col_mid, col_right = st.columns([1.2, 1.5, 1.2])

# ------------------------------------------
# COLONNA 1: TACTICAL WAR ROOM
# ------------------------------------------
with col_left:
    st.header("🚀 Tactical War Room")
    with st.container():
        st.subheader("Decision Engine")
        pot = st.number_input("Piatto Totale", value=1000, step=100)
        call = st.number_input("Costo Call", value=500, step=50)
        outs = st.slider("I tuoi Outs", 1, 21, 9)
        fase = st.selectbox("Fase della mano", ["Flop (x4)", "Turn (x2)"])
        
        # Calcolo Equity vs Odds
        eq = outs * 4 if "Flop" in fase else outs * 2
        odds = (call / (pot + call)) * 100 if (pot+call) > 0 else 0
        diff = eq - odds
        
        st.metric("Equity REALE", f"{eq}%", delta=f"{diff:.1f}%")
        
        if call > 0:
            if eq >= odds:
                st.success(f"✅ CALL PROFITTEVOLE (+{diff:.1f}%)")
                if eq > 0:
                    implied = (call * (100/eq)) - pot - call
                    st.info(f"💎 Implied Odds: Vinci {implied:.0f} fiches dopo.")
            else:
                st.error(f"❌ FOLD MATEMATICO ({diff:.1f}%)")

    st.divider()
    st.subheader("🎯 Breakeven Bluff")
    bluff_bet = st.slider("Tua puntata in bluff", 100, 5000, 500)
    be_perc = (bluff_bet / (bluff_bet + pot)) * 100
    st.warning(f"L'avversario deve foldare il **{be_perc:.1f}%** delle volte.")

# ------------------------------------------
# COLONNA 2: SUPREME GTO MATRIX
# ------------------------------------------
with col_mid:
    st.header("📊 GTO Intelligence Grid")
    mode = st.selectbox("Seleziona Filtro Range:", 
                        ["Visualizzazione", "Open UTG", "Open BTN", "3-Bet/Squeeze", "Difesa vs Raise"])
    
    # Determiniamo quale lista usare
    target_key = "UTG_OPEN" if "UTG" in mode else "BTN_OPEN" if "BTN" in mode else "3BET" if "3-Bet" in mode else "DEFENSE" if "Difesa" in mode else None
    
    # Costruzione Griglia HTML/CSS
    grid_html = '<div class="gto-grid">'
    for r_idx, r in enumerate(RANKS):
        for c_idx, c in enumerate(RANKS):
            if r_idx == c_idx: hand, style = r+c, "pair"
            elif c_idx > r_idx: hand, style = r+c+"s", "suited"
            else: hand, style = c+r+"o", "offsuit"
            
            is_active = False
            if target_key:
                if hand in RANGES[target_key]: is_active = True
            
            cl = f"gto-cell {style}"
            if target_key:
                if "3-Bet" in mode: cl += " gto-3bet" if is_active else " gto-fold"
                else: cl += " gto-open" if is_active else " gto-fold"
            
            grid_html += f'<div class="{cl}">{hand}</div>'
    grid_html += '</div>'
    
    st.markdown(grid_html, unsafe_allow_html=True)
    st.divider()
    st.info("🔴 Coppie | 🔵 Suited | ⚫ Offsuit | 🟢/🟣 Range Attivo")

# ------------------------------------------
# COLONNA 3: AI ADVISOR & INTEL
# ------------------------------------------
with col_right:
    st.header("🤖 Neural Lab")
    
    # Board Analyzer
    with st.expander("🧬 Board Analyzer", expanded=True):
        texture = st.selectbox("Texture Flop", ["Secco (K-7-2)", "Bagnato (9-10-J)", "Accoppiato (8-8-3)"])
        forza = st.selectbox("Tua Forza", ["Aria", "Coppia Media", "Top Pair", "Mostro"])
        
        if "Secco" in texture:
            if "Aria" in forza: st.success("Punta 1/3 Pot (C-Bet)")
            else: st.info("Punta per valore")
        else:
            if "Aria" in forza: st.error("Check / Arrenditi")
            else: st.warning("Punta 3/4 Pot (Protezione)")

    # Intel Hub
    st.subheader("🕵️ Opponent Intel")
    with st.form("intel_form", clear_on_submit=True):
        n = st.text_input("Nick Avversario")
        t = st.selectbox("Tipo", ["Fish", "Reg", "Nit", "Maniaco"])
        note = st.text_input("Note veloci")
        if st.form_submit_button("REGISTRA"):
            st.session_state.opponents.append({"Nick": n, "Tipo": t, "Note": note})
    
    if st.session_state.opponents:
        st.table(pd.DataFrame(st.session_state.opponents).tail(3))

# ==========================================
# 4. FOOTER SURVIVAL MASTER
# ==========================================
st.write("---")
f1, f2, f3 = st.columns(3)
with f1:
    st.subheader("⏳ M-Ratio")
    stk = st.number_input("Tuo Stack", value=5000)
    bb = st.number_input("BB attuale", value=400)
    m = stk / (bb * 1.5)
    st.write(f"Tua autonomia: **{m:.1f} giri di tavolo**")
with f2:
    st.subheader("💰 Bankroll")
    br = st.number_input("Conto Totale", value=500)
    st.write(f"Buy-in Max Sicuro: **{br/100:.2f} €**")
with f3:
    st.subheader("🧠 Mental Check")
    tilt = st.select_slider("Stato Mentale", options=["Zen", "Calmo", "Irritato", "TILT"])
    if tilt == "TILT": st.error("🆘 CHIUDI I TAVOLI ORA!")
