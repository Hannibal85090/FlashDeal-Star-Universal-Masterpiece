from enum import Enum
from typing import List, Union
from pydantic import field_validator, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

# 1. القائمة المرجعية للموديلات (للتوثيق ورسائل الخطأ)
SUPPORTED_MODELS_LIST: List[str] = ["gemini-pro", "gpt-4", "gpt-3.5-turbo"]

class SupportedAIModels(str, Enum):
    GEMINI_PRO = "gemini-pro"
    GPT_4 = "gpt-4"
    GPT_3_5 = "gpt-3.5-turbo"

class Settings(BaseSettings):
    # إعدادات الهوية الأساسية للمشروع
    APP_NAME: str = "My FlashDeal Star"
    APP_ENV: str = "production"
    
    # إعدادات التشغيل والوسائط
    USE_MEDIA: bool = True
    MEDIA_DEVICE: str = "camera"
    USE_AI: bool = True
    
    # تحديد النوع كـ Enum صريح لضمان التوافق التام
    AI_MODEL: SupportedAIModels = SupportedAIModels.GEMINI_PRO

    # 2. المترجم الصريح والمحصن (The Explicit Enum Guard)
    @field_validator("AI_MODEL", mode="before")
    @classmethod
    def validate_ai_model(cls, value: Union[str, SupportedAIModels]) -> SupportedAIModels:
        """
        يضمن هذا المحقق تحويل أي مدخل نصي (من ملفات .env) إلى نوع Enum صريح
        قبل وصوله إلى محرك النظام الأساسي.
        """
        # إذا كانت القيمة بالفعل Enum، يتم إرجاعها مباشرة لضمان السرعة والتوافق
        if isinstance(value, SupportedAIModels):
            return value
            
        try:
            # التحويل الصريح من نص إلى Enum
            return SupportedAIModels(value)
        except ValueError:
            # رسالة خطأ احترافية تعرض الموديلات المتاحة لتسهيل التصحيح
            available = ", ".join(SUPPORTED_MODELS_LIST)
            raise ValueError(
                f"⚠️ القيمة '{value}' غير صالحة لـ AI_MODEL. "
                f"الخيارات المدعومة في FlashDeal هي: [{available}]"
            )

    # 3. بروتوكول إدارة البيئة المتعددة (الأولوية للأخير)
    model_config = SettingsConfigDict(
        # ترتيب القراءة: .env (قالب) ثم .env.local (تخصيص شخصي)
        env_file=[".env", ".env.local"],
        env_file_encoding="utf-8",
        extra="ignore"  # تجاهل الإعدادات الإضافية لضمان استقرار النواة
    )

# 4. كتلة التحقق والتشغيل (حارس بوابة النواة)
try:
    settings = Settings()
except ValidationError as e:
    print("\n❌ فشل نظام التحقق من إعدادات My FlashDeal Star:")
    for error in e.errors():
        # عرض المسار الدقيق للحقل ورسالة الخطأ بوضوح
        loc = " -> ".join(str(l) for l in error['loc'])
        print(f"  - [الموقع: {loc}]: {error['msg']}")
    print("\nيرجى مراجعة ملفات البيئة (.env) وتصحيح القيم.")
    raise SystemExit(1)
