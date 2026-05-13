import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from config import RTC_CONFIG  # استيراد الإعداد المركزي
from ui.components.gesture_ui import GestureUI
from controllers.main_controller import MainController
from loguru import logger

def show():
    st.header("✨ واجهة التحكم السيادية")
    
    # استدعاء المكونات مرة واحدة لتجنب تكرار الكود
    controller = MainController()
    gesture_ui = GestureUI()

    # محرك البث باستخدام الإعدادات المركزية
    webrtc_streamer(
        key="flash-gesture-engine",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIG, # استخدام الإعداد الموحد
        video_frame_callback=gesture_ui.update,
        async_processing=True,
    )

    # تنفيذ المنطق المالي بناءً على الإيماءة المكتشفة
    if st.session_state.get("last_gesture"):
        controller.process_gesture_action(st.session_state.last_gesture)

    st.divider()
    gesture_ui.display_result()

def safe_show():
    try:
        show()
    except Exception as e:
        logger.error(f"خطأ في تشغيل الواجهة: {e}")
        st.error("نعتذر، حدث خلل عارض في الاتصال.")

if __name__ == "__main__":
    safe_show()
