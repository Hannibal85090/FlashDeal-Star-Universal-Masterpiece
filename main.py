"""
⭐ FlashDeal Star Universal ⭐
V3.0 — Talk. Pay. Done.
Author: Ali Arfaoui (Hannibal85090)
"""
import streamlit as st
import time, json, hashlib
from voice_parser    import parse_voice_command
from security_engine import FlashDealTokenEngine
from vault_protection import DataVault
from config import (APP_TITLE, APP_VERSION, SLOGAN, AUTHOR,
                    SUPPORTED_CHAINS, MIN_AMOUNT, DEFAULT_CHAIN, MASTER_KEY)

# ── إعدادات الصفحة ───────────────────────────────────────────────────────────────
st.set_page_config(page_title=APP_TITLE, page_icon="⭐", layout="wide")

# ── تهيئة الجلسة (Session State) ──────────────────────────────────────────────────
if "auth" not in st.session_state:
    st.session_state.update({
        "auth": False, "token": None, "tx_log": [], 
        "vault": DataVault(), "engine": FlashDealTokenEngine()
    })

# ── الواجهة البرمجية (UI Custom CSS) ──────────────────────────────────────────────
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #020b18 0%, #050f2c 100%); color: #e0e0e0; }
    .stButton>button { background: linear-gradient(45deg, #1a6fe8, #00e5ff); color: white; border: none; border-radius: 10px; }
    .card { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; border: 1px solid rgba(0, 229, 255, 0.2); }
</style>
""", unsafe_allow_html=True)

# ── الهيدر (Header) ───────────────────────────────────────────────────────────
st.title(APP_TITLE)
st.caption(f"{SLOGAN} | {APP_VERSION} by {AUTHOR}")

# ── شريط التنقل (Navigation) ──────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🏠 الرئيسية", "🎙️ الأمر الصوتي", "🛡️ الأمن والخزنة"])

with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"### العميل المالي السيادي (SFA)")
        st.info("جاهز لتنفيذ عمليات الدفع المتناهية الصغر (Nanopayments) عبر 11 شبكة.")
    with col2:
        if st.button("توليد توكن الأمان المتبادل"):
            st.session_state.token = st.session_state.engine.generate_mutual_token("User_01", MASTER_KEY)
            st.success("تم توليد التوكن بنجاح!")

with tab2:
    st.subheader("تحدث أو اكتب أمرك المالي")
    cmd = st.text_input("مثال: ادفع 0.000001 ميكروسنت عبر شبكة بوليغون")
    if cmd:
        result = parse_voice_command(cmd)
        st.json(result)
        if result['intent'] == 'pay':
            st.balloons()
            st.success(f"تمت عملية الدفع بقيمة {result['amount']} على شبكة {result['chain']}")

with tab3:
    st.subheader("خزنة البيانات المحمية")
    key = st.text_input("مفتاح التخزين")
    val = st.text_input("القيمة المراد حمايتها")
    if st.button("حفظ في الخزنة"):
        st.session_state.vault.store(key, val, MASTER_KEY)
        st.write("تم التشفير والتخزين بنجاح.")

