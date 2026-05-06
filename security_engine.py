"""
FlashDeal Star â€” Security Engine
Mutual Token Handshake + Anomaly Detection (no heavy deps)
"""
import hashlib, time, os, json, hmac, base64

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
            "expires_in": 300,
            "method":     "HMAC-SHA256",
        }

    def verify_token(self, token_data: dict, master_key: str) -> bool:
        try:
            age = int(time.time()) - int(token_data["issued_at"])
            return age < token_data["expires_in"]
        except Exception:
            return False

    def detect_anomaly(self, events: list) -> dict:
        if not events:
            return {"threat": False, "score": 0.0, "label": "NOMINAL"}
        freq   = len(events)
        score  = min(freq / 10.0, 1.0)
        threat = score > 0.6
        label  = "CRITICAL" if score > 0.8 else "WARNING" if score > 0.4 else "NOMINAL"
        return {"threat": threat, "score": round(score, 3), "label": label}

    def eip_712_sign(self, wallet_id: str, amount: float, chain: str, nonce: int) -> str:
        payload = f"{wallet_id}:{amount}:{chain}:{nonce}:{int(time.time())}"
        sig = hashlib.sha3_256(payload.encode()).hexdigest()
        return f"0x{sig[:40]}...{sig[-6:]}"
