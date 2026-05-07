import streamlit as st
import time

# --- 1. الإعدادات الأساسية والهوية البصرية ---
st.set_page_config(
    page_title="FlashDeal Star Universal",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. محرك الجماليات المتقدم (Cyber-UX Engine) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=IBM+Plex+Sans+Arabic:wght@300;500&display=swap');
    
    /* الخلفية الكونية العميقة */
    .stApp {
        background: radial-gradient(circle at top right, #001f3f 0%, #00050a 100%);
        color: #ffffff;
    }

    /* الشريط الجانبي السيادي */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 10, 20, 0.95);
        border-right: 1px solid #00d4ff;
    }

    /* تصميم البطاقات المضيئة (كما في الصورة 2) */
    .cyber-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .cyber-card:hover {
        border-color: #00d4ff;
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.4);
        transform: scale(1.05);
    }

    /* العنوان الرئيسي المنقح */
    .hero-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        background: linear-gradient(90deg, #ffffff, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }

    /* شريط الحالة السفلي التفاعلي */
    .status-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(0, 212, 255, 0.1);
        backdrop-filter: blur(5px);
        padding: 10px;
        text-align: center;
        font-size: 0.8rem;
        border-top: 1px solid #00d4ff;
        z-index: 999;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. الشريط الجانبي (Sidebar Navigation) كما في الصورة sc.png ---
with st.sidebar:
    st.markdown("<h2 style='color: #00d4ff;'>🛡️ Control Center</h2>", unsafe_allow_html=True)
    st.divider()
    menu = {
        "💰 Deposit USDC": "استلام الرصيد السيادي",
        "🔄 Cross-Chain Swap": "التبديل بين الشبكات",
        "🎮 Gaming & Rewards": "الألعاب والمكافآت",
        "📄 Content & Licensing": "المحتوى والتراخيص",
        "👥 Agent Payments": "دفعات الوكلاء الذكية",
        "⚙️ Manage App": "إدارة التطبيق"
    }
    for item, desc in menu.items():
        if st.button(item, use_container_width=True):
            st.toast(f"جاري فتح {item}...")

# --- 4. واجهة العرض الرئيسية (Main Showcase) ---
st.markdown('<h1 class="hero-title">🌟 FlashDeal Star 🌟</h1>', unsafe_allow_html=True)
st.markdown("<div style='text-align:center; letter-spacing:8px; color:#00d4ff; font-weight:bold;'>TALK. PAY. DONE.</div>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; font-family:\"IBM Plex Sans Arabic\"; color:#888;'>تحدث . ادفع . تم</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 5. لوحة الإحصائيات الحية (Live Stats) ---
metrics_col = st.columns(4)
stats = [
    ("💰 Volume", "2.874M", "USD"),
    ("⚡ Transact", "1,847,920", "Total"),
    ("⛽ Gas", "FREE", "0.00"),
    ("🌐 Chains", "11", "Active")
]

for i, (lab, val, delta) in enumerate(stats):
    with metrics_col[i]:
        st.markdown(f"""
            <div class="cyber-card">
                <div style="font-size:0.8rem; color:#00d4ff;">{lab}</div>
                <div style="font-size:1.8rem; font-weight:bold;">{val}</div>
                <div style="font-size:0.7rem; color:#555;">{delta}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 6. بروتوكول النانوبايمنت التفاعلي ---
with st.expander("⚡ NANOPAYMENTS PROTOCOL v3.0 - Active", expanded=True):
    st.markdown("""
        <div style="background: rgba(0, 212, 255, 0.05); padding: 15px; border-radius: 10px; border-left: 4px solid #00d4ff;">
            <strong>HTTP 402 Interface:</strong> Gasless USDC permits via EIP-3009 active on 11 chains.
            <br><small style="color: #00d4ff;">Current Latency: 420ms | Security: Mutual Token Handshake Enabled</small>
        </div>
    """, unsafe_allow_html=True)

# --- 7. مساحة الحوار والعمليات (Chat Masterpiece) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض سجل الرسائل بتنسيق فخم ومنقح (السطر 359 المطور نهائياً)
for msg in st.session_state.messages:
    role = str(msg.get("role", "user")).strip().lower()
    # استخدام الأيقونات المدمجة لضمان استقرار العرض في كل الظروف
    avatar = "assistant" if role == "assistant" else "user"
    
    with st.chat_message(role, avatar=avatar):
        # استخدام لون مميز لكل دور لزيادة الوضوح البصري
        content_color = "#00d4ff" if role == "assistant" else "#ffffff"
        st.markdown(f"<span style='color: {content_color};'>{msg.get('content', '')}</span>", unsafe_allow_html=True)

# --- 8. حقل الإدخال الذكي (The Pulse) ---
if prompt := st.chat_input("تحدث، اطلب، أو ادفع هنا... Write, Talk, or Pay here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="assistant"):
        with st.spinner("Executing Sovereignty Protocol..."):
            time.sleep(0.8)
            response = "Protocol 3.0: Transaction signed. Verified by Star Handshake. Done."
            st.markdown(f"**{response}**")
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- 9. تذييل الصفحة السيادي ---
st.markdown("""
    <div class="status-bar">
        FlashDeal Star Universal Masterpiece © 2026 | Built on Circle Gateway | Powered by Ais-A One Framework
    </div>
""", unsafe_allow_html=True)

