import av
import time
import csv
import os
from loguru import logger
import streamlit as st
from services.gesture_recognition.recognizer import GestureRecognizer

# اختيار بسيط لنموذج لإشعار صوتي (محاولة دون اعتمادات خارجية)
def play_beep():
    try:
        # Windows
        if os.name == "nt":
            import winsound
            winsound.Beep(1000, 120)
        else:
            # macOS/Linux: حاول وجود aplay/afplay
            if os.system("which afplay > /dev/null 2>&1") == 0:
                os.system("afplay /System/Library/Sounds/Glass.aiff &> /dev/null &")
            elif os.system("which aplay > /dev/null 2>&1") == 0:
                os.system("aplay /usr/share/sounds/alsa/Front_Left.wav &> /dev/null &")
    except Exception:
        pass

class GestureUI:
    def __init__(self):
        self.recognizer = GestureRecognizer()

        if "last_gesture" not in st.session_state:
            st.session_state.last_gesture = None
        if "last_update_time" not in st.session_state:
            st.session_state.last_update_time = {}
        if "confidence_history" not in st.session_state:
            st.session_state.confidence_history = []

        # تبريد مخصص لكل إيماءة (يمكنك تغيير القيم حسب الإيماءات المتوقعة)
        self.cooldown_map = {
            "thumbs_up": 1.0,
            "peace": 1.8,
            "fist": 2.0,
        }

        self.display_timeout = 2.0
        self.log_file = "gesture_log.csv"
        # تأكد من وجود الملف
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "gesture", "confidence"])

        self.high_confidence_threshold = 0.92

    def update(self, frame):
        try:
            img = frame.to_ndarray(format="bgr24")
        except Exception as e:
            logger.error(f" خطأ في تحويل الإطار: {e}")
            return frame

        results = self.recognizer.recognize(img)

        if results and isinstance(results, dict) and results.get("gestures"):
            current_gesture = results["gestures"][0]
            current_confidence = results.get("confidence", 0.90)
            now = time.time()

            # تبريد مخصص حسب الإيماءة
            cooldown = self.cooldown_map.get(current_gesture, 1.0)
            last_ts = st.session_state.last_update_time.get(current_gesture, 0)

            if (now - last_ts) < cooldown:
                return frame

            # تحديث البيانات
            st.session_state.last_gesture = current_gesture
            st.session_state.last_update_time[current_gesture] = now
            st.session_state.confidence_history.append(current_confidence)

            # حفظ السجل
            with open(self.log_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), current_gesture, current_confidence])

            # إشعار صوتي عند الثقة العالية
            if current_confidence >= self.high_confidence_threshold:
                play_beep()

            # احتفاظ بثقة آخر للإحصاء العابر
            st.session_state.last_gesture = current_gesture
        else:
            if time.time() - st.session_state.last_update_time.get(st.session_state.last_gesture, 0) > self.display_timeout:
                st.session_state.last_gesture = None

        return frame

    def display_result(self):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric(label="حالة الرصد", value="نشط ")

        with col2:
            if st.session_state.last_gesture:
                last = st.session_state.last_gesture
                recent = st.session_state.confidence_history[-5:] if st.session_state.confidence_history else []
                avg_conf = sum(recent) / len(recent) if recent else 0
                st.success(f" المكتشف: {last}")
                st.caption(f"متوسط الثقة (آخر 5): {avg_conf:.2f}")
                if avg_conf >= self.high_confidence_threshold:
                    st.toast("إيماءة عالية الثقة!", icon="")
            else:
                st.info(" بانتظار إيماءة...")
