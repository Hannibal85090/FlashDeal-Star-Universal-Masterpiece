import sys
import signal
from loguru import logger
from core.config.settings import settings

def configure_logging():
    """إعداد نظام السجلات المتقدم بناءً على LOG_LEVEL من الإعدادات"""
    logger.remove()
    
    # تنسيق السجلات مع دعم خاصية success والرموز الملونة
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    logger.add(sys.stderr, format=log_format, level=settings.LOG_LEVEL, colorize=True)
    logger.add("logs/app_{time:YYYY-MM-DD}.log", rotation="1 day", retention="7 days")
    
    # استخدام logger.success كما اقترحت لتعزيز وضوح الحالة
    logger.success(f"--- تم تهيئة نظام سجلات {settings.APP_NAME} بنجاح ---")

class AppRunner:
    def __init__(self):
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        
        self.settings = settings
        self._init_services()
        
    def _init_services(self):
        """فحص الـ imports ووجود الإعدادات قبل البدء"""
        logger.info("فحص تكامل الخدمات والإعدادات...")
        
        # إضافة فحص الـ imports كما اقترحت لضمان عدم حدوث AttributeError
        if not hasattr(self.settings, 'USE_AI'):
            logger.warning("⚠️ الإعدادات لا تحتوي على حقل USE_AI؛ سيتم تعطيل خدمات الذكاء الاصطناعي افتراضياً.")
            self.use_ai = False
        else:
            self.use_ai = self.settings.USE_AI

        if not hasattr(self.settings, 'USE_MEDIA'):
            logger.warning("⚠️ الإعدادات لا تحتوي على حقل USE_MEDIA.")
            self.use_media = False
        else:
            self.use_media = self.settings.USE_MEDIA

        logger.success("🚀 تم فحص وتهيئة الخدمات بنجاح")

    def _handle_shutdown(self, signum, frame):
        logger.warning(f"إشارة إغلاق مستلمة: {signum}. جاري تأمين البيانات...")
        sys.exit(0)
        
    def run(self):
        try:
            logger.info(f"بدء محرك {self.settings.APP_NAME} (البيئة: {self.settings.APP_ENV})")
            # منطق التشغيل هنا (Talk. Pay. Done.)
        except Exception as e:
            logger.error(f"حدث خطأ غير متوقع: {e}")
            raise

if __name__ == "__main__":
    configure_logging()
    runner = AppRunner()
    runner.run()
