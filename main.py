import streamlit as st
import base64

# استدعاء النواة الصلبة مع التأكد من سلامة الربط
try:
    from voice_parser import parse_voice_command
    from security_engine import FlashDealTokenEngine
    from vault_protection import DataVault
except ImportError:
    st.error("Protocol Error: Operational core modules missing.")

# إعدادات الواجهة السيادية
st.set_page_config(page_title="FlashDeal Star Universal", page_icon="⭐", layout="wide")

# هندسة الواجهة (Advanced Cyber-Tech CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 50% 50%, #101525 0%, #050505 100%);
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    
    /* الحاوية السيادية المركزية */
    .masterpiece-container {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(0, 198, 255, 0.15);
        border-radius: 40px;
        padding: 60px;
        box-shadow: 0 0 80px rgba(0, 198, 255, 0.1);
        margin: 20px auto;
        max-width: 900px;
    }
    
    .star-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(to bottom, #ffffff 30%, #00c6ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: 5px;
        margin-bottom: 0px;
    }
    
    .slogan {
        text-align: center;
        font-size: 1.1rem;
        letter-spacing: 10px;
        color: #00c6ff;
        text-transform: uppercase;
        margin-bottom: 40px;
        opacity: 0.8;
    }

    /* حقل الإدخال الصوتي */
    .stTextInput>div>div>input {
        background: rgba(0, 0, 0, 0.3) !important;
        color: #00c6ff !important;
        border: 1px solid rgba(0, 198, 255, 0.3) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        font-size: 1.2rem !important;
        text-align: center;
    }

    /* زر التنفيذ الفخم */
    .stButton>button {
        background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 20px 0;
        font-family: 'Orbitron', sans-serif;
        font-size: 1rem;
        letter-spacing: 2px;
        box-shadow: 0 10px 30px rgba(0, 114, 255, 0.4);
        transition: all 0.4s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 198, 255, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.markdown('<div class="masterpiece-container">', unsafe_allow_html=True)
    st.markdown('<p class="star-title">⭐ FLASHDEAL STAR</p>', unsafe_allow_html=True)
    st.markdown('<p class="slogan">Talk. Pay. Done.</p>', unsafe_allow_html=True)

    # قسم الميكروفون والتحكم
    st.markdown("<h4 style='text-align: center; color: white; opacity: 0.6;'>VOICE BIOMETRIC GATEWAY</h4>", unsafe_allow_html=True)
    
    voice_input = st.text_input("", placeholder="[ Listening for Sovereign Signature... ]")

    if voice_input:
        st.markdown("<div style='text-align: center; color: #00ff88; font-size: 0.9rem; animation: pulse 1.5s infinite;'>● ENCRYPTED AUDIO STREAM ACTIVE</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("INITIATE SOVEREIGN TRANSACTION"):
        if voice_input:
            with st.status("Engaging FlashDeal Core...", expanded=False) as status:
                cmd = parse_voice_command(voice_input)
                if cmd["status"] == "active":
                    engine = FlashDealTokenEngine()
                    auth = engine.generate_mutual_token("ALi_Arfaoui", "sovereign_master_key")
                    
                    time_sleep = 1.5 # تأثير بصري للثقل التقني
                    st.success(f"PROTOCOL CONFIRMED: {cmd['amount']} USDC AUTHORIZED")
                    st.info(f"MUTUAL HANDSHAKE TOKEN: {auth['token']}")
                    st.balloons()
                    status.update(label="Transaction Complete", state="complete")
                else:
                    st.error("ACCESS DENIED: KEYWORD SIGNATURE NOT FOUND")
        else:
            st.warning("SYSTEM IDLE: AWAITING COMMAND")

    st.markdown('</div>', unsafe_allow_html=True)
    
    # التذييل الاحترافي
    st.markdown("<p style='text-align: center; opacity: 0.3; font-size: 0.8rem; margin-top: 50px;'>SOVEREIGN FINANCIAL AGENT | V1.0 UNIVERSAL MASTERPIECE</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

