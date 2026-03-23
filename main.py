import streamlit as st
import random

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="WAR MACHINE OMEGA", layout="wide", page_icon="🔱")

# --- CSS PROFESSIONALE PER GRIGLIA FISSA (MOBILE FRIENDLY) ---
st.markdown("""
<style>
    .stApp { background-color: #020202; color: #00ffcc; }
    
    /* Forza la griglia a 13 colonne anche su telefono */
    .gto-container {
        display: grid;
        grid-template-columns: repeat(13, 1fr);
        gap: 2px;
        width: 100%;
        max-width: 600px;
        margin: 0 auto;
    }
    
    .gto-cell {
        aspect-ratio: 1 / 1;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 2px;
        font-size: 7px;
        font-weight: bold;
        color: white;
        text-align: center;
    }
    
    .pair { background: #ff1744; }
    .suited { background: #2979ff; }
    .offsuit { background: #263238; border: 0.1px solid #37474f; }
    .gto-open { background: #00e676 !important; color: black !important; box-shadow: 0 0 8px #00e676; border: 1px solid white !important; }
    .gto-fold { opacity: 0.15; filter: grayscale(100%); }
    
    .stMetric { border: 1px solid #00ffcc; border-radius: 12px; background: rgba(0,255,204,0.05); padding: 10px; }
</style>
""", unsafe_allow_html=True)

# --- DATABASE RANGE GTO ---
RANGES = {
    "UTG": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "AKs", "AQs", "AJs", "ATs", "AKo", "AQo", "KQs"],
    "HJ": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "AKs", "AQs", "AJs", "ATs", "A9s", "AKo", "AQo", "KQs", "KJs", "QJs", "JTs"],
    "BTN": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22", 
            "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
            "AKo", "AQo", "AJo", "ATo", "A9o", "A8o", "A7o", "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s",
            "KJo", "KTo", "QJs", "QTs", "Q9s", "QTo", "JTs", "J9s", "T9s", "98s", "87s", "76s", "65s", "54s"]
}
RANKS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

# --- SIDEBAR ---
st.sidebar.markdown("<h1 style='color: #00ffcc; text-align: center;'>🔱 OMEGA</h1>", unsafe_allow_html=True)
menu = st.sidebar.selectbox("MODULI:", ["📊 GTO MATRIX", "🚀 WAR ROOM", "🎓 ARENA", "⏳ MASTER"])

# ==========================================
# 1. GTO MATRIX (FIXED GRID VERSION)
# ==========================================
if menu == "📊 GTO MATRIX":
    st.title("📊 GTO Interactive Matrix")
    pos_mode = st.selectbox("Posizione:", ["Nessuno", "UTG", "HJ", "BTN"])
    
    # Costruiamo la griglia HTML
    grid_html = '<div class="gto-container">'
    
    for r_idx, r in enumerate(RANKS):
        for c_idx, c in enumerate(RANKS):
            if r_idx == c_idx: hand, style = r+c, "pair"
            elif c_idx > r_idx: hand, style = r+c+"s", "suited"
            else: hand, style = c+r+"o", "offsuit"
            
            is_active = pos_mode != "Nessuno" and hand in RANGES.get(pos_mode, [])
            
            cell_class = f"gto-cell {style}"
            if pos_mode != "Nessuno":
                cell_class += " gto-open" if is_active else " gto-fold"
            
            grid_html += f'<div class="{cell_class}">{hand}</div>'
    
    grid_html += '</div>'
    
    # Visualizza la griglia
    st.markdown(grid_html, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("🤖 AI Advisor")
    sel_h = st.selectbox("Analizza mano:", [r+c if r==c else r+c+"s" if RANKS.index(c)>RANKS.index(r) else c+r+"o" for r in RANKS for c in RANKS])
    if any(sel_h in RANGES[k] for k in RANGES):
        st.success(f"✅ OPEN: {sel_h} è forte.")
    else:
        st.error(f"❌ FOLD: {sel_h} è debole.")

# ==========================================
# 2. WAR ROOM (ODDS)
# ==========================================
elif menu == "🚀 WAR ROOM":
    st.title("🚀 Tactical War Room")
    pot = st.number_input("Piatto", value=1000)
    call = st.number_input("Costo Call", value=500)
    eq = st.slider("Tua Equity %", 0, 100, 35)
    odds = (call / (pot + call)) * 100 if (pot+call) > 0 else 0
    st.metric("Pot Odds richieste", f"{odds:.1f}%")
    if eq >= odds: st.success("✅ CHIAMA")
    else: st.error("❌ PASSA")

elif menu == "🎓 TITAN TRAINING":
    st.title("🎓 Titan Training Lab")
    if st.button("SFERRA UN ATTACCO ⚡"):
        st.session_state.t_bb = random.randint(5, 25)
        st.session_state.t_h = random.choice(["AA", "72o", "KJs", "44", "A5s", "QTo", "98s", "J5s", "K-Q off"])
        st.session_state.t_pos = random.choice(["UTG", "BTN", "SB"])
        # Logica IA avanzata
        bb, mano, pos = st.session_state.t_bb, st.session_state.t_h, st.session_state.t_pos
        is_p = (bb < 12 or mano == "AA" or (bb < 15 and "K" in mano and pos == "BTN") or (mano == "44" and pos == "SB"))
        st.session_state.t_ans = "PUSH" if is_p else "FOLD"
    
    if 't_bb' in st.session_state:
        st.subheader(f"STACK: {st.session_state.t_bb} BB | MANO: {st.session_state.t_h} | POS: {st.session_state.t_pos}")
        c1, c2 = st.columns(2)
        if c1.button("🔥 ALL-IN"):
            if st.session_state.t_ans == "PUSH": st.success("🎯 BERSAGLIO DISTRUTTO!"); st.session_state.score += 1
            else: st.error("💀 SEI STATO ELIMINATO!")
            st.session_state.total += 1
        if c2.button("📁 FOLD"):
            if st.session_state.t_ans == "FOLD": st.success("🎯 DISCIPLINA DI FERRO!"); st.session_state.score += 1
            else: st.error("💀 HAI PERSO VALORE!")
            st.session_state.total += 1
        st.sidebar.metric("Precisione Titan", f"{st.session_state.score}/{st.session_state.total}")

# ==========================================
# MODULO 4: NEURAL EXPLOIT LAB (CHICCA!)
# ==========================================
elif menu == "👺 NEURAL EXPLOIT LAB":
    st.title("👺 Exploitative Intelligence Lab")
    action = st.selectbox("L'avversario ha fatto:", ["Limp da UTG", "Mini-raise dal Bottone", "Donk-bet al Flop", "Check-Raise gigante"])
    
    st.markdown(f'<div class="exploit-card"><b>PROFILO PROBABILE:</b> {"Amatore Passivo" if "Limp" in action else "Manezzone Aggressivo"}</div>', unsafe_allow_html=True)
    st.subheader("🛡️ Risposta del Dio:")
    if "Limp" in action: st.info("Isola rilanciando 4x con mani medie. Prendi il piatto subito.")
    if "Bottone" in action: st.info("Difendi il BB in modo aggressivo. Il suo range è larghissimo.")
    if "Donk-bet" in action: st.warning("Spesso è debolezza. Rilancia per farlo foldare se il board è secco.")

# ==========================================
# MODULO 5 & 6: CHRONOS & REVENUE
# ==========================================
elif menu == "⏳ CHRONOS (M-Ratio)":
    st.title("⏳ Chronos Survival Timer")
    s, b, a = st.number_input("Stack", value=5000), st.number_input("BB", value=400), st.number_input("Ante", value=400)
    m = s / (b + (b/2) + a)
    st.metric("Tua Vita (M-Ratio)", f"{m:.1f}")
    st.progress(min(m/20, 1.0))
    if m < 6: st.error("PROTOCOLLO PUSH/FOLD ATTIVO.")

elif menu == "💰 REVENUE CONTROL":
    st.title("💰 Revenue & Bankroll Control")
    br = st.number_input("Capitale Totale (€)", value=500)
    st.metric("Buy-in Max (Safe Mode)", f"{br/100:.2f} €")
    st.metric("Buy-in Max (Aggressive)", f"{br/50:.2f} €")
