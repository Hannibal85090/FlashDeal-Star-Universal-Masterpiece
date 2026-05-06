import hashlib
import secrets
import time
from config import TOKEN_EXPIRY

class FlashDealTokenEngine:
    def __init__(self):
        self.expiry = TOKEN_EXPIRY

    def generate_mutual_token(self, user_id, biometric_hash):
        # تدقيق صارم للأقواس والصيغ الرياضية لضمان عدم التعليق
        try:
            timestamp = str(int(time.time() // self.expiry))
            seed = f"{user_id}:{biometric_hash}:{timestamp}"
            server_secret = secrets.token_hex(16)
            token_value = hashlib.sha256(f"{seed}:{server_secret}".encode()).hexdigest()
            return {"token": token_value, "timestamp": timestamp, "status": "SECURE"}
        except Exception:
            return {"token": None, "status": "ERROR"}

    def verify_auth(self, input_code, stored_hash):
        if not input_code or not stored_hash:
            return False
        input_hash = hashlib.sha256(input_code.encode()).hexdigest()
        return input_hash == stored_hash

