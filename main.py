"""
â­گ FlashDeal Star Universal â­گ
V3.0 â€” Talk. Pay. Done.
Author: Ali Arfaoui (Hannibal85090)
"""
import streamlit as st
import time, json, hashlib, random, string
from datetime import datetime

from voice_parser    import parse_voice_command
from security_engine import FlashDealTokenEngine
from vault_protection import DataVault
from config import (APP_TITLE, APP_VERSION, SLOGAN, AUTHOR,
                    SUPPORTED_CHAINS, MIN_AMOUNT, DEFAULT_CHAIN, MASTER_KEY,
                    ALSA_BASE_URL, ALSA_API_KEY)

# â”€â”€ Page config â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.set_page_config(page_title="â­گ FlashDeal Star â­گ", page_icon="â­گ", layout="wide",
                   initial_sidebar_state="collapsed")

# â”€â”€ Session state defaults â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
for k, v in {"auth": False, "token": None, "tx_log": [], "vault": DataVault(),
              "engine": FlashDealTokenEngine(), "anomaly_events": [],
              "tab": "home"}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# â”€â”€ CSS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');

/* â”€â”€ Base â”€â”€ */
html, body, [class*="css"] { font-family: 'Exo 2', sans-serif; }
.stApp { background: radial-gradient(ellipse at 20% 10%, #0a1628 0%, #020b18 60%, #010810 100%); color: #ddeeff; }
.block-container { padding: 1rem 1.5rem 4rem; max-width: 860px; margin: 0 auto; }
section[data-testid="stSidebar"] { display: none; }

/* â”€â”€ Hero â”€â”€ */
.hero-box {
    background: linear-gradient(145deg, #080f1e, #0d1c38);
    border: 1px solid rgba(66,197,245,.25);
    border-radius: 22px;
    padding: 2.4rem 1.6rem 2rem;
    text-align: center;
    box-shadow: 0 0 50px rgba(26,111,232,.15);
    margin-bottom: 1.2rem;
}
.star-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(1.8rem, 5vw, 2.8rem);
    font-weight: 900;
    background: linear-gradient(135deg, #ffffff 30%, #42c5f5 80%, #00e5ff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: 4px; margin-bottom: .2rem;
}
.slogan-txt {
    font-size: .95rem; letter-spacing: 6px; color: #42c5f5;
    text-transform: uppercase; opacity: .85; margin-bottom: 1rem;
}
.version-badge {
    display: inline-block; background: rgba(26,111,232,.18);
    border: 1px solid rgba(66,197,245,.3); border-radius: 20px;
    padding: 3px 14px; font-size: .75rem; color: #42c5f5;
    font-family: 'Orbitron', monospace; letter-spacing: 1px;
}

/* â”€â”€ Nav tabs â”€â”€ */
.nav-row { display: flex; gap: 8px; margin-bottom: 1rem; flex-wrap: wrap; }
.nav-btn {
    flex: 1; min-width: 90px;
    background: rgba(12,28,50,.8); border: 1px solid rgba(66,197,245,.15);
    border-radius: 12px; padding: .55rem .4rem; text-align: center;
    font-size: .78rem; font-weight: 600; color: #5a8aaa; cursor: pointer;
    transition: all .2s; font-family: 'Exo 2', sans-serif;
}
.nav-btn.active { background: rgba(26,111,232,.22); border-color: rgba(66,197,245,.5); color: #42c5f5; }

/* â”€â”€ Cards â”€â”€ */
.card {
    background: #0c1c32; border: 1px solid rgba(66,197,245,.12);
    border-radius: 16px; padding: 1.2rem; margin-bottom: .9rem;
}
.card.glow { border-color: rgba(66,197,245,.3); box-shadow: 0 0 28px rgba(26,111,232,.12); }
.card-title { font-family: 'Orbitron', monospace; font-size: .75rem; color: #42c5f5; letter-spacing: 2px; margin-bottom: .8rem; }

/* â”€â”€ Metric â”€â”€ */
.metric-row { display: flex; gap: .6rem; margin-bottom: .9rem; flex-wrap: wrap; }
.metric { flex: 1; min-width: 80px; background: #0c1c32; border: 1px solid rgba(66,197,245,.1); border-radius: 12px; padding: .9rem .5rem; text-align: center; }
.metric-val { font-family: 'Orbitron', monospace; font-size: 1rem; font-weight: 700; color: #00e5ff; display: block; }
.metric-lbl { font-size: .68rem; color: #3a5a7a; margin-top: 3px; display: block; }

/* â”€â”€ Log â”€â”€ */
.tx-row { display: flex; align-items: center; gap: .6rem; padding: .6rem .8rem; border-bottom: 1px solid rgba(66,197,245,.07); font-size: .8rem; }
.tx-row:last-child { border-bottom: none; }
.tx-hash { font-family: 'Courier New', monospace; color: #42c5f5; font-size: .75rem; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.tx-amt-pos { color: #00e676; font-family: 'Orbitron', monospace; font-size: .78rem; }
.tx-amt-neg { color: #ff4060; font-family: 'Orbitron', monospace; font-size: .78rem; }

/* â”€â”€ Status pills â”€â”€ */
.pill { display: inline-block; border-radius: 20px; padding: 2px 12px; font-size: .7rem; font-weight: 600; }
.pill-ok  { background: rgba(0,230,118,.12); color: #00e676; border: 1px solid rgba(0,230,118,.25); }
.pill-warn{ background: rgba(255,215,64,.12); color: #ffd740; border: 1px solid rgba(255,215,64,.25); }
.pill-bad { background: rgba(255,64,96,.12);  color: #ff4060; border: 1px solid rgba(255,64,96,.25); }

/* â”€â”€ Streamlit overrides â”€â”€ */
div[data-testid="stTextInput"] input {
    background: #0c1c32 !important; color: #42c5f5 !important;
    border: 1px solid rgba(66,197,245,.3) !important; border-radius: 12px !important;
    font-family: 'Exo 2', sans-serif !important; font-size: 1rem !important;
}
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #1a6fe8, #0a3d8a) !important;
    color: white !important; border: none !important; border-radius: 12px !important;
    font-family: 'Orbitron', monospace !important; letter-spacing: 1.5px !important;
    box-shadow: 0 4px 22px rgba(26,111,232,.35) !important; transition: all .2s !important;
}
div[data-testid="stSelectbox"] select, div[data-testid="stNumberInput"] input {
    background: #0c1c32 !important; color: #ddeeff !important;
    border: 1px solid rgba(66,197,245,.2) !important; border-radius: 10px !important;
}
div[data-testid="stTabs"] button { font-family: 'Orbitron', monospace !important; font-size: .7rem !important; letter-spacing: 1px !important; }
.stAlert { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# â”€â”€ Helper: random tx hash â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def rand_hash():
    return "0x" + "".join(random.choices(string.hexdigits.lower(), k=40))

# â”€â”€ Helper: log tx â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def log_tx(amount, chain, dest, status="confirmed"):
    st.session_state.tx_log.insert(0, {
        "hash": rand_hash(), "amount": amount, "chain": chain,
        "dest": dest[:14] + "â€¦" if len(dest) > 14 else dest,
        "status": status, "ts": datetime.now().strftime("%H:%M:%S"),
    })
    st.session_state.tx_log = st.session_state.tx_log[:20]

# â”€â”€ HERO â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown(f"""
<div class="hero-box">
  <div class="star-title">â­گ FlashDeal Star â­گ</div>
  <div class="slogan-txt">{SLOGAN}</div>
  <span class="version-badge">{APP_VERSION} آ· Circle Gateway آ· aisa.one</span>
</div>
""", unsafe_allow_html=True)

# â”€â”€ TABS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
tab_home, tab_pay, tab_security, tab_ai, tab_vault, tab_cases = st.tabs([
    "ًںڈ  Home", "âڑ، Pay", "ًں›، Security", "ًں¤– OsoBot", "ًں”’ Vault", "ًں“± Cases"
])

# â•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گ
# TAB 1 â€” HOME
# â•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گ
with tab_home:
    # Live metrics
    vol  = round(2.84 + random.random() * .05, 3)
    txc  = random.randint(1847293, 1848000)
    st.markdown(f"""
    <div class="metric-row">
      <div class="metric"><span class="metric-val">{vol}M</span><span class="metric-lbl">Volume USD</span></div>
      <div class="metric"><span class="metric-val">{txc:,}</span><span class="metric-lbl">Transactions</span></div>
      <div class="metric"><span class="metric-val" style="color:#00e676;">FREE</span><span class="metric-lbl">Gas Fees</span></div>
      <div class="metric"><span class="metric-val">11</span><span class="metric-lbl">Chains</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Protocol info
    st.markdown("""
    <div class="card glow">
      <div class="card-title">â¬، NANOPAYMENTS PROTOCOL</div>
      <p style="font-size:.85rem;color:#7ab3d4;line-height:1.8;">
        <b style="color:#42c5f5;">HTTP 402</b> + <b style="color:#42c5f5;">EIP-3009</b> gasless USDC permits.<br>
        Min transaction: <b style="color:#00e5ff;">$0.000001</b> آ· Confirmation: <b style="color:#00e5ff;">&lt;500ms</b><br>
        Chains: Polygon آ· Sei آ· Ethereum آ· Solana آ· Avalanche آ· Base
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Recent txs
    if st.session_state.tx_log:
        st.markdown('<div class="card"><div class="card-title">ًں“‹ RECENT TRANSACTIONS</div>', unsafe_allow_html=True)
        for tx in st.session_state.tx_log[:5]:
            color = "tx-amt-pos" if tx["status"] == "confirmed" else "tx-amt-neg"
            pill  = "pill-ok" if tx["status"] == "confirmed" else "pill-bad"
            st.markdown(f"""
            <div class="tx-row">
              <span class="tx-hash">{tx['hash']}</span>
              <span class="{color}">+${tx['amount']:.6f}</span>
              <span style="font-size:.72rem;color:#3a5a7a;">{tx['chain']}</span>
              <span class="pill {pill}">{tx['status']}</span>
              <span style="font-size:.68rem;color:#2a4a6a;">{tx['ts']}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="card" style="text-align:center;color:#2a4a6a;font-size:.85rem;">No transactions yet â€” send your first nanopayment âڑ،</div>', unsafe_allow_html=True)

# â•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گ
# TAB 2 â€” PAY
# â•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گ
with tab_pay:
    st.markdown('<div class="card glow"><div class="card-title">âڑ، VOICE COMMAND GATEWAY</div>', unsafe_allow_html=True)
    voice = st.text_input("", placeholder="[ ط§ط¯ظپط¹ 0.001 USDC ط¹ظ„ظ‰ Sei | pay 0.001 USDC on Sei ]", key="voice_in")
    if voice:
        cmd = parse_voice_command(voice)
        cols = st.columns(3)
        cols[0].metric("Intent",  cmd["intent"].upper())
        cols[1].metric("Amount",  f"${cmd['amount']:.6f}")
        cols[2].metric("Chain",   cmd["chain"].capitalize())
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">ًں”§ MANUAL PAYMENT</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    dest_addr = c1.text_input("Destination Address", value="0x_FLASHDEAL_VAULT", key="dest")
    chain_sel = c2.selectbox("Chain", SUPPORTED_CHAINS, index=0, key="chain_sel")
    amount_in = st.number_input("Amount (USDC)", min_value=MIN_AMOUNT, value=0.000042,
                                 step=MIN_AMOUNT, format="%.6f", key="amount_in")

    if st.button("ًں”گ  VERIFY & SEND NANOPAYMENT  âڑ،", key="send_btn"):
        with st.status("âڑ™ Engaging FlashDeal Coreâ€¦", expanded=True) as status:
            # biometric gate simulation
            st.write("ًں”گ Biometric gate checkâ€¦"); time.sleep(.4)
            st.write("ًں”— Connecting to Circle Gatewayâ€¦"); time.sleep(.4)
            st.write("ًں“، HTTP 402 handshakeâ€¦"); time.sleep(.35)
            # token
            tkn = st.session_state.engine.generate_mutual_token("Ali_Arfaoui", MASTER_KEY)
            st.session_state.token = tkn
            st.write(f"âœچï¸ڈ EIP-3009 permit signed â€” nonce: `{tkn['nonce'][:12]}â€¦`"); time.sleep(.35)
            # ALSA payment simulation
            sig = st.session_state.engine.eip_712_sign(dest_addr, amount_in, chain_sel, random.randint(1000,9999))
            st.write(f"ًں“¤ Broadcasting to {chain_sel.capitalize()}â€¦"); time.sleep(.4)
            st.write("âœ… On-chain verificationâ€¦"); time.sleep(.35)
            confirm_ms = random.randint(340, 490)
            log_tx(amount_in, chain_sel, dest_addr)
            st.session_state.anomaly_events.append(time.time())
            st.session_state.vault.store("last_tx", {"amount": amount_in, "chain": chain_sel, "sig": sig})
            status.update(label=f"âœ… Confirmed in {confirm_ms}ms â€” Gas: FREE", state="complete")

        st.success(f"âœ… **{amount_in:.6f} USDC** sent on **{chain_sel.capitalize()}** â€” `{sig}`")
        st.info(f"ًں”گ Mutual Token: `{tkn['token']}`")
        st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)

    # TX log in pay tab
    if st.session_state.tx_log:
        st.markdown('<div class="card"><div class="card-title">ًں“‹ TX LOG</div>', unsafe_allow_html=True)
        for tx in st.session_state.tx_log[:6]:
            st.markdown(f"""<div class="tx-row">
              <span class="tx-hash">{tx['hash']}</span>
              <span class="tx-amt-pos">+${tx['amount']:.6f}</span>
              <span style="font-size:.72rem;color:#3a5a7a;">{tx['chain']}</span>
              <span class="pill pill-ok">{tx['status']}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# â•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گ
# TAB 3 â€” SECURITY
# â•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گ
with tab_security:
    engine = st.session_state.engine
    anomaly = engine.detect_anomaly(st.session_state.anomaly_events)
    shield = "ARMED" if not anomaly["threat"] else "ALERT"
    pill_cls = "pill-ok" if shield == "ARMED" else "pill-bad"

    st.markdown(f"""
    <div class="card" style="border-color:rgba(0,230,118,.25);">
      <div style="display:flex;align-items:center;gap:.8rem;margin-bottom:1rem;">
        <span style="font-size:1.8rem;">ًں›،ï¸ڈ</span>
        <div>
          <div style="font-size:.95rem;font-weight:600;color:#00e676;">Quantum-Safe Shield</div>
          <div style="font-size:.72rem;color:#3a6a8a;margin-top:2px;">EIP-712 آ· Replay Protection آ· Multi-Sig Vault</div>
        </div>
        <span class="pill {pill_cls}" style="margin-left:auto;">{shield}</span>
      </div>
      <div class="metric-row">
        <div class="metric"><span class="metric-val" style="color:{'#00e676' if not anomaly['threat'] else '#ff4060'};">{len(st.session_state.anomaly_events)}</span><span class="metric-lbl">Events</span></div>
        <div class="metric"><span class="metric-val">{anomaly['score']}</span><span class="metric-lbl">Threat Score</span></div>
        <div class="metric"><span class="metric-val" style="color:#00e676;">99.7%</span><span class="metric-lbl">Trust</span></div>
        <div class="metric"><span class="metric-val" style="color:#42c5f5;">&lt;50ms</span><span class="metric-lbl">Detect</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Gesture recognition display
    st.markdown('<div class="card"><div class="card-title">ًں¤ڑ GESTURE RECOGNITION â€” ISL SUPPORT</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size:.82rem;color:#5a8aaa;margin-bottom:.8rem;">
    ط§ط¶ط؛ط· ط¹ظ„ظ‰ ط¥ط´ط§ط±ط© ظ„ظ„طھط­ظ‚ظ‚ ظ…ظ† ط§ظ„طھط¹ط±ظپ ط¹ظ„ظٹظ‡ط§ (ظ…ط­ط§ظƒط§ط© â€” ط§ظ„ظƒط§ظ…ظٹط±ط§ ط§ظ„ط­ظ‚ظٹظ‚ظٹط© ظپظٹ ظ†ط³ط®ط© ط§ظ„ط¬ظ‡ط§ط²)
    </p>
    """, unsafe_allow_html=True)

    g_cols = st.columns(4)
    gestures = [("ًں‘‹","Wave\nظ…ط±ط­ط¨ط§ظ‹"),("âœŒï¸ڈ","Peace\nط³ظ„ط§ظ…"),("ًں‘Œ","OK\nظ…ظˆط§ظپظ‚"),("ًں¤ں","ILY\nط£ط­ط¨ظƒ")]
    for col, (ico, lbl) in zip(g_cols, gestures):
        with col:
            if st.button(f"{ico}\n{lbl}", key=f"g_{ico}"):
                st.success(f"âœ… {lbl.split()[0]} ظ…ظڈط¹طھط±ظپ ط¨ظ‡")
                st.session_state.anomaly_events.append(time.time())

    g_cols2 = st.columns(4)
    gestures2 = [("âœ‹","Stop\nطھظˆظ‚ظپ"),("âک‌ï¸ڈ","Point\nط§ط®طھط±"),("ًں‘چ","Approve"),("âœٹ","Reject")]
    for col, (ico, lbl) in zip(g_cols2, gestures2):
        with col:
            if st.button(f"{ico}\n{lbl}", key=f"g2_{ico}"):
                st.success(f"âœ… {lbl.split()[0]} ظ…ظڈط¹طھط±ظپ ط¨ظ‡")
    st.markdown('</div>', unsafe_allow_html=True)

    # Simulate attack
    st.markdown('<div class="card"><div class="card-title">âڑ ï¸ڈ ATTACK SIMULATION</div>', unsafe_allow_html=True)
    if st.button("ًںڑ¨  Simulate Replay Attack  (Test Defense)", key="attack_btn"):
        with st.status("Simulating attackâ€¦", expanded=True) as s:
            st.write("ًںڑ¨ Replay attack detected â€” nonce: 0x0000 (DUPLICATE)"); time.sleep(.6)
            st.write("ًں›،ï¸ڈ Replay rejected â€” nonce already consumed"); time.sleep(.5)
            st.write("ًں”’ Wallet frozen for 30s â€” anomaly window"); time.sleep(.5)
            st.write("âœ… Threat neutralized â€” shield restored"); time.sleep(.3)
            s.update(label="âœ… Attack blocked â€” Shield ARMED", state="complete")
        st.error("ًںڑ¨ Attack detected and neutralized in 487ms")
        st.success("âœ… EIP-3009 replay protection worked correctly")
    st.markdown('</div>', unsafe_allow_html=True)

    # Token display
    if st.session_state.token:
        tkn = st.session_state.token
        st.markdown(f"""
        <div class="card"><div class="card-title">ًں”‘ ACTIVE MUTUAL TOKEN</div>
        <div style="font-family:'Courier New',monospace;font-size:.78rem;color:#42c5f5;line-height:1.9;">
        Token:   <b>{tkn['token']}</b><br>
        User:    {tkn['user']}<br>
        Nonce:   {tkn['nonce'][:16]}â€¦<br>
        Method:  {tkn['method']}<br>
        Expires: {tkn['expires_in']}s
        </div></div>
        """, unsafe_allow_html=True)

# â•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گ
# TAB 4 â€” OSOBOT AI  (aisa.one)
# â•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گ
with tab_ai:
    st.markdown('<div class="card glow"><div class="card-title">ًں¤– OSOBOT â€” SOVEREIGN AI AGENT (aisa.one)</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <p style="font-size:.82rem;color:#7ab3d4;margin-bottom:.8rem;">
    OsoBot is powered by <b style="color:#42c5f5;">ALSA on aisa.one</b>.
    Ask anything about Nanopayments, EIP-3009, x402, or FlashDeal Star.
    ط§ط³ط£ظ„ ط¨ط§ظ„ط¹ط±ط¨ظٹط© ط£ظˆ ط§ظ„ط¥ظ†ط¬ظ„ظٹط²ظٹط© ط£ظˆ ط§ظ„ظپط±ظ†ط³ظٹط©.
    </p>
    """, unsafe_allow_html=True)

    # Chat history
    if "chat_hist" not in st.session_state:
        st.session_state.chat_hist = [
            {"role": "assistant", "content": "ظ…ط±ط­ط¨ط§ظ‹! ط£ظ†ط§ OsoBot âڑ،ًں¤–\nظˆظƒظٹظ„ظƒ ط§ظ„ظ…ط§ظ„ظٹ ط§ظ„ط°ظƒظٹ. ط£ط³طھط·ظٹط¹ ظ…ط³ط§ط¹ط¯طھظƒ ظپظٹ x402, EIP-3009, Circle Gateway ظˆFlashDeal Star.\nط¨ظ…ط§ط°ط§ ظٹظ…ظƒظ†ظ†ظٹ ظ…ط³ط§ط¹ط¯طھظƒطں"}
        ]

    # Display history
    for msg in st.session_state.chat_hist[-12:]:
        with st.chat_message(msg["role"], avatar="â­گ" if msg["role"] == "assistant" else "ًں‘¤"):
            st.markdown(msg["content"])

    # Quick prompts
    st.markdown('<div style="display:flex;gap:.4rem;flex-wrap:wrap;margin:.4rem 0;">', unsafe_allow_html=True)
    qcols = st.columns(3)
    quick = [("x402 Protocol", "ظ…ط§ ظ‡ظˆ ط¨ط±ظˆطھظˆظƒظˆظ„ x402 ظˆظƒظٹظپ ظٹط¹ظ…ظ„طں"),
             ("EIP-3009 Code",  "ط§ظƒطھط¨ ظƒظˆط¯ Python ظ„ط¥ط±ط³ط§ظ„ USDC ط¹ط¨ط± EIP-3009"),
             ("Sei vs Polygon", "ظ…ط§ ط§ظ„ظپط±ظ‚ ط¨ظٹظ† Sei ظˆ Polygon ظ„ظ„ط¯ظپط¹طں")]
    for col, (lbl, prompt) in zip(qcols, quick):
        with col:
            if st.button(lbl, key=f"q_{lbl}"):
                st.session_state.chat_hist.append({"role": "user", "content": prompt})
                st.rerun()

    # User input
    user_msg = st.chat_input("ط§ط³ط£ظ„ OsoBotâ€¦ | Ask OsoBotâ€¦")
    if user_msg:
        st.session_state.chat_hist.append({"role": "user", "content": user_msg})

        # Call ALSA / aisa.one
        import urllib.request
        reply = ""
        if ALSA_API_KEY:
            try:
                payload = json.dumps({
                    "model": "alsa-1",
                    "messages": [
                        {"role": "system", "content": (
                            "You are OsoBot, the expert AI financial agent for FlashDeal Star â€” "
                            "a micropayment platform on Circle Gateway. Expert in HTTP 402, x402, "
                            "EIP-3009 gasless USDC, 11-chain cross-chain payments, biometric EIP-712 security. "
                            "Respond in the same language as the user (Arabic/French/English/German/Italian). "
                            "Be concise and write real runnable code when asked."
                        )},
                        *[{"role": m["role"], "content": m["content"]}
                          for m in st.session_state.chat_hist[-8:]]
                    ],
                    "max_tokens": 800,
                }).encode()
                req = urllib.request.Request(
                    f"{ALSA_BASE_URL}/chat/completions",
                    data=payload,
                    headers={"Content-Type": "application/json", "Authorization": f"Bearer {ALSA_API_KEY}"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=20) as resp:
                    data = json.loads(resp.read())
                    reply = data["choices"][0]["message"]["content"]
            except Exception as e:
                reply = f"âڑ ï¸ڈ aisa.one API error: {e}\n\nDemo answer: For EIP-3009 payments, use `transferWithAuthorization(from, to, value, nonce, deadline, v, r, s)` on-chain."
        else:
            # Offline demo answers
            answers = {
                "x402": "ط¨ط±ظˆطھظˆظƒظˆظ„ x402 ظ‡ظˆ ظ…ط¹ظٹط§ط± Web Monetization ظٹط³طھط®ط¯ظ… HTTP 402 ظ„طھظ…ظƒظٹظ† ط§ظ„ط¢ظ„ط§طھ ظ…ظ† ط§ظ„ط¯ظپط¹ طھظ„ظ‚ط§ط¦ظٹط§ظ‹. ط¹ظ†ط¯ظ…ط§ طھط·ظ„ط¨ ظˆظƒظٹظ„ AI ظ…ظˆط§ط±ط¯ ظ…ط¯ظپظˆط¹ط©طŒ ظٹط³طھط¬ظٹط¨ ط§ظ„ط®ط§ط¯ظ… ط¨ظ€ `402 Payment Required` ظ…ط¹ ط±ط£ط³ `X-Payment` ظٹط­ط¯ط¯ ط§ظ„ظ…ط¨ظ„ط؛ ظˆط§ظ„ط¹ظ…ظ„ط© ظˆط§ظ„ط´ط¨ظƒط©.",
                "eip": "```python\n# EIP-3009 gasless transfer\nfrom web3 import Web3\nw3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))\n\ndef sign_eip3009(from_addr, to_addr, value, nonce, deadline, private_key):\n    domain = {'name':'USD Coin','version':'2','chainId':137,'verifyingContract':USDC_ADDR}\n    types = {'TransferWithAuthorization':[{'name':'from','type':'address'},{'name':'to','type':'address'},{'name':'value','type':'uint256'},{'name':'nonce','type':'bytes32'},{'name':'deadline','type':'uint256'}]}\n    msg = {'from':from_addr,'to':to_addr,'value':value,'nonce':nonce,'deadline':deadline}\n    return w3.eth.account.sign_typed_data(private_key, domain, types, msg)\n```",
                "default": f"OsoBot ط¬ط§ظ‡ط² ظ„ظ„ظ…ط³ط§ط¹ط¯ط©! ظٹظ…ظƒظ†ظ†ظٹ ط´ط±ط­:\nâ€¢ ط¨ط±ظˆطھظˆظƒظˆظ„ **x402** ظˆ **HTTP 402**\nâ€¢ ظƒظˆط¯ **EIP-3009** ظ„ط¥ط±ط³ط§ظ„ USDC ط¨ط¯ظˆظ† ط؛ط§ط²\nâ€¢ ظ…ظ‚ط§ط±ظ†ط© ط´ط¨ظƒط§طھ ط§ظ„ط¨ظ„ظˆظƒط´ظٹظ† ظ„ظ„ظ…ط¯ظپظˆط¹ط§طھ ط§ظ„ط°ط±ظٹط©\nâ€¢ طھظƒط§ظ…ظ„ **Circle Gateway** ظ…ط¹ FlashDeal Star\n\nط§ط³ط£ظ„ ط¨ط§ظ„ط¹ط±ط¨ظٹط© ط£ظˆ ط§ظ„ط¥ظ†ط¬ظ„ظٹط²ظٹط© ط£ظˆ ط§ظ„ظپط±ظ†ط³ظٹط©! ًںڑ€"
            }
            u = user_msg.lower()
            if any(k in u for k in ["x402","402","http"]):
                reply = answers["x402"]
            elif any(k in u for k in ["eip","code","ظƒظˆط¯","python"]):
                reply = answers["eip"]
            else:
                reply = answers["default"]

        st.session_state.chat_hist.append({"role": "assistant", "content": reply})
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# â•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گ
# TAB 5 â€” VAULT
# â•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گ
with tab_vault:
    vault = st.session_state.vault

    st.markdown('<div class="card" style="border-color:rgba(0,230,118,.2);"><div class="card-title">ًں”’ SOVEREIGN DATA VAULT</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    vkey = c1.text_input("Key", value="user_profile", key="vk")
    vsec = c2.text_input("Secret", value="sovereign", type="password", key="vs")
    vval = st.text_area("Value (JSON)", value='{"user":"Ali_Arfaoui","tier":"sovereign"}', height=80, key="vv")

    col_s, col_r, col_w = st.columns(3)
    if col_s.button("ًں’¾ Store", key="vstore"):
        try:
            vault.store(vkey, json.loads(vval), vsec)
            st.success("âœ… Stored securely")
        except json.JSONDecodeError:
            st.error("Invalid JSON")

    if col_r.button("ًں”چ Retrieve", key="vread"):
        res = vault.retrieve(vkey, vsec)
        if res:
            st.json(res)
        else:
            st.warning("Key not found or wrong secret")

    if col_w.button("ًں—‘ Wipe Vault", key="vwipe"):
        vault.wipe(vsec)
        st.success("Vault wiped")

    st.markdown('</div>', unsafe_allow_html=True)

    # Audit log
    log = vault.audit_log()
    if log:
        st.markdown('<div class="card"><div class="card-title">ًں“‹ VAULT AUDIT LOG</div>', unsafe_allow_html=True)
        for entry in log[-8:]:
            ts = datetime.fromtimestamp(entry["ts"]).strftime("%H:%M:%S")
            color = "#00e676" if entry["action"]=="READ" else "#ffd740" if entry["action"]=="WRITE" else "#ff4060"
            st.markdown(f'<div class="tx-row"><span style="font-family:\'Courier New\',monospace;color:{color};font-size:.78rem;">[{ts}] {entry["action"]}</span><span class="tx-hash">{entry.get("key","")}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# â•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گ
# TAB 6 â€” USE CASES
# â•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گ
with tab_cases:
    cases = [
        ("ًں¤–", "Agent & API Payments", "AI agents autonomously detect HTTP 402, sign EIP-3009 permits, and pay â€” no human loop. Perfect for LLM inference APIs and autonomous trading bots."),
        ("ًں“ٹ", "Data & Analytics Markets", "Pay-per-query data marketplace. Each SQL query or price feed costs fractions of a cent. No subscriptions â€” instant USDC settlement."),
        ("ًںژ®", "Gaming & Micro-Rewards", "Real in-game economies. Reward $0.000050 per achievement, charge $0.001 for power-ups. Cross-platform via 11 chains."),
        ("ًں“„", "Content & Licensing", "Per-article, per-image, per-song payments at scale. HTTP 402 gates content at the protocol level. No platform cut."),
        ("ًںژ“", "MIGA Education (NAVIGAA)", "Pedagogical tools by Ali Arfaoui. Arabic orthography + grammar, math discovery logic, and multilingual AI tutoring."),
        ("ًں’³", "FlashDeal SIM Card", "My FlashDeal Star hardware ecosystem. Secure SIM connectivity, smart-proximity car integration (Star Key), adaptive secret code logic."),
    ]

    for i in range(0, len(cases), 2):
        c1, c2 = st.columns(2)
        for col, (ico, title, desc) in zip([c1, c2], cases[i:i+2]):
            with col:
                st.markdown(f"""
                <div class="card" style="cursor:pointer;">
                  <div style="font-size:1.6rem;margin-bottom:.5rem;">{ico}</div>
                  <div style="font-size:.88rem;font-weight:600;color:#ddeeff;margin-bottom:.4rem;">{title}</div>
                  <div style="font-size:.78rem;color:#5a8aaa;line-height:1.65;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

# â”€â”€ Footer â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown(f"""
<div style="text-align:center;opacity:.3;font-size:.72rem;margin-top:2rem;padding-bottom:1rem;">
  {APP_TITLE} آ· {APP_VERSION} آ· {AUTHOR}<br>
  Sovereign Financial Agent آ· Circle Gateway آ· aisa.one آ· EIP-3009 آ· HTTP 402
</div>
""", unsafe_allow_html=True)
