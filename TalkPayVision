import streamlit as st
import speech_recognition as sr
import cv2
import mediapipe as mp
import numpy as np
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# ============================================
# 1. تحميل المفاتيح من ملف .env
# ============================================
load_dotenv()
API_KEY = os.getenv("API_KEY")   # المفتاح مخزن في ملف .env
API_URL = "https://console.aisa.one/api/v1/execute"

# ============================================
# 2. إدارة الحالة (Session State)
# ============================================
if 'balance' not in st.session_state:
    st.session_state.balance = 1000.0
if 'command_history' not in st.session_state:
    st.session_state.command_history = []

# ============================================
# 3. وحدة الصوت (محلي فقط)
# ============================================
def listen_to_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.toast("🎙️ جاري الاستماع...")
        try:
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio, language="ar-AR")
        except:
            return None

# ============================================
# 4. وحدة الإيماءات (Mediapipe)
# ============================================
class HandGestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils

    def detect(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        gesture = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_TIP]

                if thumb_tip.y < index_tip.y:
                    gesture = "👍 Like"
                else:
                    gesture = "✋ Stop"

        return frame, gesture

# ============================================
# 5. ربط مع API aisa.one
# ============================================
def send_to_api(command):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"command": command, "balance": st.session_state.balance}
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# ============================================
# 6. واجهة المستخدم
# ============================================
st.title("⚡ FlashDeal Star Universal")
st.write("Talk. Pay. Done.")

col1, col2 = st.columns([2, 1])

# --- قسم الإيماءات ---
with col1:
    st.subheader("📸 Gesture & Vision")
    img_file = st.camera_input("التقط صورة إيماءة (Like/Stop)")
    
    if img_file:
        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)

        detector = HandGestureDetector()
        frame, gesture = detector.detect(frame)

        if gesture:
            st.success(f"تم التعرف على الإيماءة: {gesture}")
            st.session_state.command_history.append(f"إيماءة: {gesture}")

            # منطق مالي مباشر
            if gesture == "👍 Like":
                st.session_state.balance += 100
                st.info("✅ تمت إضافة 100 USDC")
            elif gesture == "✋ Stop":
                st.warning("⏸️ تم إيقاف العملية")

            # إرسال للـ API
            api_response = send_to_api(gesture)
            st.json(api_response)

        st.image(frame, channels="BGR")

# --- قسم الصوت ---
with col2:
    st.subheader("🎤 Voice Control")
    if st.button("🎤 ابدأ الاستماع للصوت"):
        cmd = listen_to_command()
        if cmd:
            st.info(f"الأمر المكتشف: {cmd}")
            st.session_state.command_history.append(f"صوت: {cmd}")
            api_response = send_to_api(cmd)
            st.json(api_response)
        else:
            st.warning("لم يتم اكتشاف صوت، حاول مجدداً")

# --- عرض الرصيد ---
st.markdown(f"<div style='font-size:1.5rem;color:#00d4ff;text-align:center;padding:10px;'>💰 Balance: {st.session_state.balance} USDC</div>", unsafe_allow_html=True)

# --- سجل العمليات ---
st.divider()
st.subheader("📜 Audit Log (Sovereign History)")
for item in reversed(st.session_state.command_history[-5:]):
    st.write(f"🔹 {item}")
