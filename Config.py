# config.py

"""
FlashDeal Star - Central Configuration
"""

import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import SecretStr

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./payments.db"
    API_TITLE: str = "My FlashDeal Star Backend"
    API_VERSION: str = "1.0.0"
    SECRET_KEY: SecretStr = SecretStr("SOVEREIGN_SECRET_KEY_2026")  # استخدام SecretStr لإخفاء القيمة

    class Config:
        case_sensitive = True
        env_file = ".env"  # تحميل القيم من ملف .env

@lru_cache()
def get_settings() -> Settings:
    """Retrieve the application settings."""
    return Settings()
