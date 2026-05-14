from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime, timedelta
import secrets
import hashlib
import os
from loguru import logger
from pydantic_settings import BaseSettings
from pydantic import SecretStr

# --------------------- 1. الإعدادات ---------------------
class Settings(BaseSettings):
    SECRET_KEY: SecretStr = "flashdeal-secret-key" # تأكد من مطابقته للواجهة
    DATABASE_URL: str = "sqlite:///./flashdeal.db"
    TOKEN_EXPIRE_MINUTES: int = 15
    
    class Config:
        env_file = ".env"

settings = Settings()
app = FastAPI(title="My FlashDeal Star Sovereign API", version="1.0.0")
security = HTTPBearer()

# --------------------- 2. النماذج (Models) ---------------------
class SovereignPaymentRequest(BaseModel):
    method: str
    metadata: Dict
    hash: str
    timestamp: str

class PaymentResponse(BaseModel):
    status: str
    token: str
    payment_id: str
    expires_at: str
    message: Optional[str] = None

# --------------------- 3. إدارة التوكنات ---------------------
class MutualTokenManager:
    def __init__(self):
        # توكن مبدئي للتجربة (Debug Token)
        self.token_store = {
            "FLASHDEAL-ADMIN-DEBUG": {
                "payment_id": "SYSTEM-INIT",
                "expires_at": datetime.now() + timedelta(days=1),
                "method": "SYSTEM",
                "valid": True
            }
        }
    
    def generate_token(self, payment_id: str, method: str) -> str:
        token = f"FD-{secrets.token_hex(8).upper()}"
        expires_at = datetime.now() + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
        self.token_store[token] = {
            "payment_id": payment_id,
            "expires_at": expires_at,
            "method": method,
            "valid": True
        }
        return token
    
    def validate_token(self, token: str) -> bool:
        data = self.token_store.get(token)
        return data and data["valid"] and datetime.now() < data["expires_at"]

token_manager = MutualTokenManager()

# --------------------- 4. نقاط النهاية (Endpoints) ---------------------

@app.get("/health")
async def health():
    return {"status": "online", "security": "Triple-Lock Active"}

@app.post("/api/payment", response_model=PaymentResponse)
async def handle_payment(
    request: SovereignPaymentRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # 1. فحص التوكن
    if not token_manager.validate_token(credentials.credentials):
        raise HTTPException(status_code=401, detail="Invalid Token")
    
    # 2. فحص الهاش السيادي
    expected_hash = hashlib.sha256(f"{settings.SECRET_KEY.get_secret_value()}{request.timestamp}".encode()).hexdigest()
    if request.hash != expected_hash:
        raise HTTPException(status_code=403, detail="Sovereign Access Denied")

    # 3. معالجة الدفع وإصدار توكن جديد
    payment_id = f"PYMT-{secrets.token_hex(6)}"
    new_token = token_manager.generate_token(payment_id, request.method)
    
    return PaymentResponse(
        status="success",
        token=new_token,
        payment_id=payment_id,
        expires_at=token_manager.token_store[new_token]["expires_at"].isoformat(),
        message="تمت العملية بنجاح"
    )

@app.post("/api/voice-payment", response_model=PaymentResponse)
async def handle_voice(audio: UploadFile = File(...), credentials: HTTPAuthorizationCredentials = Depends(security)):
    # منطق معالجة الصوت المختصر
    payment_id = f"VOICE-{secrets.token_hex(4)}"
    new_token = token_manager.generate_token(payment_id, "VOICE")
    return PaymentResponse(status="success", token=new_token, payment_id=payment_id, 
                           expires_at=token_manager.token_store[new_token]["expires_at"].isoformat())
