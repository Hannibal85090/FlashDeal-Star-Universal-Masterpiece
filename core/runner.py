import logging
from loguru import logger
import sys

def configure_logging():
    logger.add(
        sys.stderr,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO"
    )

class AppRunner:
    def __init__(self):
        self._load_config()
        self._init_services()
        
    def _load_config(self):
        from core.config import settings
        self.settings = settings
        
    def _init_services(self):
        from services import MediaService, AIService
        self.media = MediaService() if self.settings.USE_MEDIA else None
        self.ai = AIService() if self.settings.USE_AI else None
        
    def run(self):
        try:
            logger.info("Starting AI Agent Application")
            # تنفيذ التطبيق هنا
        except Exception as e:
            logger.error(f"Application failed: {e}")
            raise
