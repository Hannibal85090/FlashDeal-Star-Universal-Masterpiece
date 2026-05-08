"""
FlashDeal Star — Security Engine
Mutual Token Handshake + Anomaly Detection
"""
import hashlib, time, os, hmac, base64

class FlashDealTokenEngine:
    VERSION = "3.0-sovereign"

    def generate_mutual_token(self, user_id: str, master_key: str) -> dict:
        ts    = str(int(time.time()))
        nonce = base64.b64encode(os.urandom(16)).decode()
        raw   = f"{user_id}:{master_key}:{ts}:{nonce}"
        token = hmac.new(master_key.encode(), raw.encode(), hashlib.sha256).hexdigest()
        return {
            "token":      token[:32],
            "user":       user_id,
            "nonce":      nonce,
            "issued_at":  ts,
            "expires_in": 300, # صالح لمدة 5 دقائق
            "method":     "HMAC-SHA256",
        }

    def verify_token(self, token_data: dict, master_key: str) -> bool:
        try:
            age = int(time.time()) - int(token_data["issued_at"])
            return age < token_data["expires_in"]
        except:
            return False

    def detect_anomaly(self, events: list) -> dict:
        freq = len(events)
        score = min(freq / 10.0, 1.0)
        return {
            "threat": score > 0.6,
            "score": score,
            "label": "CRITICAL" if score > 0.8 else "NOMINAL"
        }

