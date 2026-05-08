import streamlit as st
import time
from voice_parser import parse_voice_command

# -- إعدادات الواجهة الاحترافية --
st.set_page_config(page_title="FlashDeal Star Universal", page_icon="⭐", layout="wide")

# -- إضافة CSS مخصص للتصميم الزجاجي (Cyber-UI) --
st.markdown("""
<style>
    .main {
        background: radial-gradient(circle at top, #0a192f, #020c1b);
    }
    .stApp {
        background-color: transparent;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(0, 229, 255, 0.2);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        transition: transform 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: #00e5ff;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #1a6fe8, #00e5ff);
        color: white;
        border: none;
        padding: 12px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# -- الهيدر التفاعلي --
st.markdown("<h1 style='text-align: center; color: #00e5ff; font-family: Orbitron;'>⭐ FLASHDEAL STAR ⭐</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #5a8aaa;'>Talk. Pay. Done. | العميل المالي السيادي</p>", unsafe_allow_html=True)

# -- تقسيم الواجهة إلى أعمدة تفاعلية --
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🎙️ مركز التحكم الصوتي")
    user_input = st.text_input("قل شيئاً (مثلاً: ادفع 10 ميكروسنت)...", placeholder="أدخل أمرك المالي هنا")
    
    if user_input:
        with st.spinner('جاري تحليل الأمر المالي...'):
            time.sleep(1) # محاكاة معالجة AI
            result = parse_voice_command(user_input)
            
            if result['intent'] == 'pay':
                st.success(f"✅ تم تأكيد العملية: إرسال {result['amount']} عبر شبكة {result['chain']}")
                st.balloons()
            else:
                st.warning("⚠️ لم أتعرف على الأمر، حاول مرة أخرى.")
    st.markdown('</div>', unsafe_allow_html=True)

# -- عرض لوحة البيانات (Dashboard) تحتها --
st.write("---")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric(label="حالة الشبكة", value="Polygon", delta="متصل (Active)")
with c2:
    st.metric(label="آخر عملية نانو", value="$0.000005", delta="ناجحة")
with c3:
    st.metric(label="الأمان", value="المستوى 3", delta="محمي حيوياً")
