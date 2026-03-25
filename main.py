import streamlit as st
import pandas as pd
import uuid

# ==========================================
# 1. CONFIGURAZIONE BUSINESS & PAYWALL
# ==========================================
st.set_page_config(page_title="PROMETHEUS POKER APEX", layout="wide", page_icon="🧿")

if 'LICENSES' not in st.session_state:
    st.session_state.LICENSES = {
        "BOSS-000": {"user": "Admin", "device_id": None},
        "VIP-001": {"user": "Cliente1", "device_id": None},
    }

if 'my_device_id' not in st.session_state:
    st.session_state.my_device_id = str(uuid.uuid4())

def check_license():
    if st.session_state.get("logged_in", False): return True
    st.markdown("<h1 style='text-align: center; color: #00e5ff; margin-top: 80px; text-shadow: 0 0 20px #00e5ff;'>🧿 PROMETHEUS APEX</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; font-size: 18px;'>Professional Tournament Engine</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div style="background: #111; padding: 30px; border-radius: 15px; border: 1px solid #333; box-shadow: 0 10px 30px rgba(0,0,0,0.8);">', unsafe_allow_html=True)
        code_input = st.text_input("Inserisci Chiave di Licenza", type="password")
        if st.button("SBLOCCA SISTEMA", use_container_width=True):
            if code_input in st.session_state.LICENSES:
                db_device = st.session_state.LICENSES[code_input]["device_id"]
                if db_device is None or db_device == st.session_state.my_device_id:
                    st.session_state.LICENSES[code_input]["device_id"] = st.session_state.my_device_id
                    st.session_state["logged_in"] = True
                    st.rerun()
                else: st.error("❌ ACCESSO NEGATO: Licenza in uso su altro dispositivo.")
            else: st.error("❌ LICENZA NON VALIDA.")
        st.markdown('</div>', unsafe_allow_html=True)
    return False

if not check_license(): st.stop()

# ==========================================
# 2. DESIGN PREMIUM (APEX THEME)
# ==========================================
st.markdown("""
<style>
    .stApp { background-color: #06080a; color: #e2e8f0; }
    .gto-container { display: grid; grid-template-columns: repeat(13, 1fr); gap: 2px; max-width: 600px; margin: 0 auto; background: #0a0c10; padding: 10px; border-radius: 10px; border: 1px solid #1e222b; }
    .gto-cell { display: flex; align-items: center; justify-content: center; aspect-ratio: 1/1; border-radius: 3px; font-size: 11px; font-weight: 800; color: #718096; background: #13161c; border: 1px solid #2d3748; transition: 0.15s; }
    .pair-base { background: #2d1318; border-color: #4a1c23; }
    .suited-base { background: #0d1b2a; border-color: #1a365d; }
    .offsuit-base { background: #1a202c; }
    .gto-open { background: #00e676 !important; color: #000 !important; box-shadow: 0 0 12px rgba(0,230,118,0.4); border-color: #69f0ae !important; z-index: 10; transform: scale(1.05); }
    .gto-push { background: #ff3d00 !important; color: #fff !important; box-shadow: 0 0 12px rgba(255,61,0,0.6); border-color: #ff8a80 !important; z-index: 10; transform: scale(1.05); }
    .metric-card { background: linear-gradient(145deg, #11141a, #0a0c10); border: 1px solid #2d3748; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .sizing-badge { display: inline-block; padding: 5px 10px; background: #1e222b; border-radius: 5px; border-left: 3px solid #00e5ff; font-weight: bold; margin-bottom: 5px;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. IL CERVELLO DEI RANGE (DEEP LEARNING)
# ==========================================
RANKS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

NASH_CORE = {
    # DEEP STACK (>40 BB)
    "Deep UTG (Apertura)": ["AA","KK","QQ","JJ","TT","99","88","77","AKs","AQs","AJs","ATs","A9s","KQs","KJs","QJs","JTs","T9s","AKo","AQo"],
    "Deep BTN (Apertura)": ["22+","A2s+","K2s+","Q4s+","J6s+","T6s+","96s+","85s+","75s+","64s+","54s","A2o+","K8o+","Q9o+","J9o+","T9o"],
    # PUSH/FOLD SHORT STACK (15 BB)
    "15bb UTG (All-In)": ["22+","A2s+","K9s+","Q9s+","J9s+","T9s","ATo+","KJo+","QJo"],
    "15bb BTN (All-In)": ["22+","A2s+","K2s+","Q2s+","J2s+","T5s+","95s+","85s+","74s+","64s+","54s","A2o+","K6o+","Q8o+","J8o+","T8o+","98o"]
}

def expand_range(range_list):
    expanded = set()
    for item in range_list:
        expanded.add(item)
        if item.endswith("+"):
            b = item[:-1]
            if len(b) == 2 and b[0] == b[1]:
                idx = RANKS.index(b[0])
                for i in range(idx + 1): expanded.add(RANKS[i] + RANKS[i])
            elif len(b) == 3:
                c1, c2, s = b[0], b[1], b[2]
                i1, i2 = RANKS.index(c1), RANKS.index(c2)
                for i in range(i2, i1, -1): expanded.add(c1 + RANKS[i] + s)
    return expanded

# ==========================================
# 4. SIDEBAR PROMETHEUS
# ==========================================
st.sidebar.markdown("<h2 style='color: #00e5ff; text-align: center; letter-spacing: 2px;'>🧿 PROMETHEUS</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-size: 10px; color: #00e676;'>SYSTEM SECURED</p>", unsafe_allow_html=True)
st.sidebar.divider()

menu = st.sidebar.radio("MODULI TATTICI:", [
    "📊 Preflop: Nash & Push/Fold", 
    "🚀 Postflop: EV & Sizing", 
    "🛡️ HUD: Opponent Exploit", 
    "💰 Finance: ICM & Bankroll"
])

# ==========================================
# MODULO 1: PREFLOP ENGINE (NASH + PUSH/FOLD)
# ==========================================
if menu == "📊 Preflop: Nash & Push/Fold":
    st.title("📊 Master Preflop Engine")
    st.write("La mappa completa per il gioco profondo e per la fase Push/Fold (Sotto i 20 BB).")
    
    col_mat, col_info = st.columns([1.8, 1])
    
    with col_mat:
        mode = st.selectbox("Seleziona Fase del Torneo e Posizione:", 
            ["Seleziona...", "Deep UTG (Apertura)", "Deep BTN (Apertura)", "15bb UTG (All-In)", "15bb BTN (All-In)"])
        
        target_key = mode if mode != "Seleziona..." else None
        active_hands = expand_range(NASH_CORE.get(target_key, [])) if target_key else set()
        
        grid_html = '<div class="gto-container">'
        for r_idx, r in enumerate(RANKS):
            for c_idx, c in enumerate(RANKS):
                if r_idx == c_idx: hand, style = r+c, "pair-base"
                elif c_idx > r_idx: hand, style = r+c+"s", "suited-base"
                else: hand, style = c+r+"o", "offsuit-base"
                
                is_active = hand in active_hands
                cl = f"gto-cell {style}"
                if target_key: 
                    if "All-In" in mode: cl += " gto-push" if is_active else " gto-fold"
                    else: cl += " gto-open" if is_active else " gto-fold"
                grid_html += f'<div class="{cl}">{hand}</div>'
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)

    with col_info:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.subheader("📏 Bet Sizing Algorithm")
        st.write("Dimensioni ottimali per rilanciare (Open Raise):")
        st.markdown('<span class="sizing-badge">Stack > 40 BB:</span> Raise 2.2x - 2.5x', unsafe_allow_html=True)
        st.markdown('<span class="sizing-badge">Stack 25-40 BB:</span> Raise 2.0x - 2.1x', unsafe_allow_html=True)
        st.markdown('<span class="sizing-badge">Stack 15-25 BB:</span> Raise Minimo (2.0x)', unsafe_allow_html=True)
        st.markdown('<span class="sizing-badge">Stack < 15 BB:</span> ALL-IN Diretto', unsafe_allow_html=True)
        
        st.divider()
        st.subheader("🎯 3-Bet Sizing (Controrilancio)")
        st.write("- **In Posizione (IP):** 3x la sua puntata.")
        st.write("- **Fuori Posizione (OOP):** 4x la sua puntata.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# MODULO 2: POSTFLOP (EV + BOARD ANALYZER)
# ==========================================
elif menu == "🚀 Postflop: EV & Sizing":
    st.title("🚀 Postflop Tactical Engine")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.subheader("🧠 Calcolo Equity (Regola 2/4)")
        outs = st.slider("Outs Vincenti", 1, 20, 9)
        fase = st.radio("Strada:", ["Flop (mancano 2 carte)", "Turn (manca 1 carta)"])
        eq = outs * 4 if "Flop" in fase else outs * 2
        st.metric("Probabilità di Vittoria", f"{eq}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.subheader("💰 Pot Odds & Call")
        pot = st.number_input("Piatto Attuale", value=1000, step=100)
        call = st.number_input("Puntata da Chiamare", value=500, step=50)
        odds = (call / (pot + call)) * 100 if (pot+call) > 0 else 0
        st.metric("Odds Matematiche Richieste", f"{odds:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    if call > 0:
        diff = eq - odds
        if diff >= 0: st.success(f"✅ CALL APPROVATO. Mossa Profittevole (+{diff:.1f}% EV).")
        else: st.error(f"❌ FOLD OBBLIGATORIO. Mossa a Perdere ({diff:.1f}% EV).")

# ==========================================
# MODULO 3 E 4: HUD, ICM E BANKROLL
# ==========================================
elif menu == "🛡️ HUD: Opponent Exploit":
    st.title("🛡️ Profilazione Avversari (Live HUD)")
    if 'ops' not in st.session_state: st.session_state.ops = []
    
    with st.form("profiler"):
        nick = st.text_input("Nickname Avversario")
        tipo = st.selectbox("Archetipo Identificato", ["Calling Station (Chiama troppo)", "Maniac (Aggredisce sempre)", "Nit (Solo mostri)", "Reg (Equilibrato)"])
        if st.form_submit_button("ACQUISISCI BERSAGLIO"):
            st.session_state.ops.append({"Target": nick, "Classe": tipo})
            st.success("Target Acquisito.")
            
    if st.session_state.ops:
        st.table(pd.DataFrame(st.session_state.ops))
        st.info("💡 **Regola d'oro:** Non bluffare MAI le Calling Station. Ruba sempre i bui ai Nit.")

elif menu == "💰 Finance: ICM & Bankroll":
    st.title("💰 Finance & Bubble Survival")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.subheader("Bankroll Manager")
        br = st.number_input("Bankroll Totale (€)", value=500.0)
        st.metric("ABI (Avg Buy-In) Sicuro", f"{br/100:.2f} €")
        st.caption("Usa la regola dell'1% per non andare mai in rovina (Broke).")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.subheader("ICM Bubble Factor")
        distanza = st.selectbox("Distanza dai premi (Bolla):", ["Lontana", "Vicina", "Scoppio Bolla (Mancano 2-3 out)"])
        if distanza == "Scoppio Bolla (Mancano 2-3 out)":
            st.error("🚨 ALLERTA ICM: Gioca chiuso. Folda anche AK se qualcuno va all-in prima di te e hai uno stack medio. Fai eliminare gli short stack.")
        else:
            st.success("🟢 ICM Normale: Gioca per accumulare fiches (ChipEV).")
        st.markdown('</div>', unsafe_allow_html=True)
