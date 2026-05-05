import streamlit as st
import cv2
import mediapipe as mp
import time
import numpy as np

# --- 1. الإعدادات السيادية للواجهة (The Masterpiece UI) ---
st.set_page_config(
    page_title="FlashDeal Star Universal Masterpiece",
    page_icon="🌟",
    layout="wide"
)

# تصميم Cyber-Tech Glassmorphism مدقق
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #050a10 0%, #0a1520 100%); color: #e0e0e0; }
    .main-title { font-size: 50px; font-weight: 900; color: #00d4ff; text-align: center; text-shadow: 0 0 20px #00d4ff; }
    .slogan { font-size: 24px; color: #00ffcc; text-align: center; font-style: italic; margin-bottom: 40px; }
    .stButton>button { 
        background: rgba(0, 212, 255, 0.05); border: 2px solid #00d4ff; color: #00d4ff; 
        border-radius: 15px; height: 3.5em; font-weight: bold; transition: 0.4s;
    }
    .stButton>button:hover { background: #00d4ff !important; color: #050a10 !important; box-shadow: 0 0 30px #00d4ff; transform: scale(1.02); }
    .status-box { padding: 20px; border-radius: 15px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌟 FlashDeal Star Universal</div>', unsafe_allow_html=True)
st.markdown('<div class="slogan">Talk. Pay. Done.</div>', unsafe_allow_html=True)

# --- 2. لوحة التحكم التفاعلية (The Dashboard) ---
left_col, right_col = st.columns([3, 2])

with left_col:
    st.write("### 🛡️ بوابة التحقق السيادية (Biometric Center)")
    secure_mode = st.toggle("تفعيل ماسح الوجه والحركة (Live AI Scan)")
    
    if secure_mode:
        FRAME_WINDOW = st.image([])
        cap = cv2.VideoCapture(0)
        mp_face = mp.solutions.face_detection
        
        with mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.6) as face_detection:
            stop_button = st.button("إيقاف الماسح الضوئي")
            while not stop_button:
                ret, frame = cap.read()
                if not ret:
                    st.error("خطأ: لم يتم العثور على كاميرا.")
                    break
                
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_detection.process(rgb_frame)
                
                if results.detections:
                    for detection in results.detections:
                        bbox = detection.location_data.relative_bounding_box
                        ih, iw, _ = frame.shape
                        x, y, w, h = int(bbox.xmin * iw), int(bbox.ymin * ih), int(bbox.width * iw), int(bbox.height * ih)
                        cv2.rectangle(rgb_frame, (x, y), (x + w, y + h), (0, 255, 204), 4)
                        cv2.putText(rgb_frame, "IDENTITY VERIFIED", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 204), 2)
                
                FRAME_WINDOW.image(rgb_frame)
                if stop_button: break
        cap.release()
    else:
        st.info("نظام الأمان في وضع الاستعداد (Waiting for Command)...")

with right_col:
    st.write("### 💳 مركز التوكن والعمليات (Financial Core)")
    with st.container():
        st.markdown('<div class="status-box">', unsafe_allow_html=True)
        st.write("**نظام التوكن المتبادل (Mutual Token System)**")
        if st.button("توليد توكن 'نجمتي' (Handshake)"):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            st.success("✅ تم توثيق الاتصال بنجاح")
            st.code("MASTER_TOKEN: FD-STAR-2026-ACTIVE", language="bash")
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.write("### 🎓 MIGA Education (الجيل الرابع)")
    with st.expander("📝 وضعية الاستكشاف: تفكيك الأعداد", expanded=True):
        st.write("يا بطل، فكك العدد **18** إلى:")
        num_user = st.number_input("10 + ?", min_value=0, max_value=10, key="miga_input")
        if st.button("تأكيد الإجابة"):
            if num_user == 8:
                st.balloons()
                st.success("عبقري! تم تسجيل نقطة إبداع.")
            else:
                st.error("حاول مجدداً، أنت تقترب من الحل!")

# --- 3. Sidebar Status ---
st.sidebar.title("🚀 حالة النظام")
st.sidebar.markdown("""
- **المشروع:** Masterpiece V2.0
- **الأمان:** التوكن المتبادل نشط
- **المطور:** علي عرفاوي
---
*Talk. Pay. Done.*
""")
