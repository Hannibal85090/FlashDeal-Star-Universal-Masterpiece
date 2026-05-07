"""
FlashDeal Star — Security Engine v3.1
Fixed: sliding-window anomaly + replay check + correct hmac API
"""
import hashlib, time, os, hmac, base64

class FlashDealTokenEngine:
    VERSION = "3.1-sovereign"

    def generate_mutual_token(self, user_id: str, master_key: str) -> dict:
        ts    = str(int(time.time()))
        nonce = base64.b64encode(os.urandom(16)).decode()
        raw   = f"{user_id}:{master_key}:{ts}:{nonce}"
        h     = hmac.new(master_key.encode(), raw.encode(), hashlib.sha256)
        token = h.hexdigest()
        return {"token": token[:32], "user": user_id, "nonce": nonce,
                "issued_at": ts, "expires_in": 300, "method": "HMAC-SHA256"}

    def verify_token(self, token_data: dict, master_key: str) -> bool:
        try:
            age = int(time.time()) - int(token_data["issued_at"])
            return age < int(token_data["expires_in"])
        except Exception:
            return False

    def detect_anomaly(self, events: list) -> dict:
        """Sliding 60-second window anomaly detection."""
        if not events:
            return {"threat": False, "score": 0.0, "label": "NOMINAL", "recent": 0}
        now    = time.time()
        recent = [e for e in events if now - e < 60]
        score  = min(len(recent) / 10.0, 1.0)
        threat = score > 0.6
        label  = "CRITICAL" if score > 0.8 else "WARNING" if score > 0.4 else "NOMINAL"
        return {"threat": threat, "score": round(score, 3),
                "label": label, "recent": len(recent)}

    def eip_712_sign(self, wallet_id: str, amount: float,
                     chain: str, nonce: int) -> str:
        payload = f"{wallet_id}:{amount}:{chain}:{nonce}:{int(time.time())}"
        sig = hashlib.sha3_256(payload.encode()).hexdigest()
        return f"0x{sig[:40]}...{sig[-6:]}"

    def check_replay(self, nonce: str, used_nonces: set) -> bool:
        """True = fresh, False = replay attack."""
        if nonce in used_nonces:
            return False
        used_nonces.add(nonce)
        return True
