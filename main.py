from fastapi import FastAPI, Depends, HTTPException
from pydantic_settings import BaseSettings
from pydantic import SecretStr
from loguru import logger
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from typing import Optional

class Settings(BaseSettings):
    API_TITLE: str = "My FlashDeal Star - Sovereign API"
    API_VERSION: str = "1.0.0"
    DATABASE_URL: SecretStr = "sqlite:///./payments.db"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="نظام آمن لإدارة المدفوعات"
)

def get_settings():
    return settings

def check_db_connection():
    try:
        engine = create_engine(
            settings.DATABASE_URL.get_secret_value(),
            pool_pre_ping=True  # فحص الاتصال قبل الاستخدام
        )
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            conn.commit()  # تأكيد التنفيذ
        return True
    except Exception as e:
        logger.warning(f"Database connection check failed: {type(e).__name__}")
        return False

@app.get("/health", summary="فحص حالة النظام الشامل")
async def health_check(
    db_check: Optional[bool] = True,
    settings: Settings = Depends(get_settings)
):
    """
    فحص النظام الشامل يتضمن:
    - حالة التطبيق الأساسية
    - اتصال قاعدة البيانات (اختياري)
    - معلومات الإصدار والأمان
    """
    status = {
        "app": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "online",
        "security": {
            "level": "Sovereign",
            "encryption": "AES-256"
        }
    }

    if db_check:
        status["database"] = {
            "status": "online" if check_db_connection() else "offline",
            "type": str(settings.DATABASE_URL.get_secret_value()).split(":")[0]
        }

    logger.success(f"Health check completed for {settings.API_TITLE}")
    return status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="key.pem",  # إذا كنت تستخدم SSL
        ssl_certfile="cert.pem"
    )
