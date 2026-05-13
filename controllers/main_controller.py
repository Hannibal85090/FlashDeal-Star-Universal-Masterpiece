# main_controller.py

import asyncio
from services.ai_service import AIService
from controllers.gesture_controller import GestureController
from controllers.sign_language_controller import SignLanguageController
from loguru import logger

class MainController:
    """المتحكم الرئيسي الذي يدمج جميع الحواس في FlashDeal Star"""
    def __init__(self):
        self.ai_service = AIService()
        self.gesture_manager = GestureController()
        self.sign_manager = SignLanguageController()
        logger.success(" تم تشغيل المنسق الرئيسي للنظام")

    async def process_multimodal_input(self, frame, voice_prompt=None, user_id="ali_001"):
        """معالجة متوازية للصوت والصورة لاتخاذ قرار مالي سريع"""
        results = {}
        
        # 1. تحليل الإيماءات (الموافقة/الإلغاء السريع)
        gesture_action = self.gesture_manager.process_interaction(frame)
        results['gesture_action'] = gesture_action

        # 2. إذا وجد صوت، نقوم بمعالجته عبر الذكاء الاصطناعي السيادي
        if voice_prompt:
            ai_response = await self.ai_service.process_sovereign_request(voice_prompt, user_id)
            results['ai_response'] = ai_response

        # 3. منطق القرار: إذا وافق المستخدم بالإيماءة والصوت
        if gesture_action == "APPROVE_ACTION":
            logger.info(f" تم تأكيد العملية للمستخدم {user_id}")
            # هنا يتم استدعاء بوابة الدفع (Talk. Pay. Done.)
            
        return results


# مثال تشغيل بسيط في حال كان هذا الملف هو نقطة الدخول
if __name__ == "__main__":
    async def main():
        mc = MainController()
        # مثال: استبدلها بإطار حقيقي وبيانات صوتية مناسبة
        dummy_frame = None
        result = await mc.process_multimodal_input(dummy_frame, voice_prompt="سعر 50 دولار", user_id="ali_001")
        print(result)

    asyncio.run(main())
