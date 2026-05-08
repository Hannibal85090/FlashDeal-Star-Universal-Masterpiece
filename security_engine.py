import hashlib, time, hmac, base64, os

class FlashDealTokenEngine:
    VERSION = "3.1-sovereign"

    def generate_mutual_token(self, user_id, master_key):
        ts = str(int(time.time()))
        nonce = base64.b64encode(os.urandom(16)).decode()
        raw = f"{user_id}:{master_key}:{ts}:{nonce}"
        h = hmac.new(master_key.encode(), raw.encode(), hashlib.sha256)
        return {"token": h.hexdigest()[:32], "user": user_id, "issued_at": ts}

    def detect_anomaly(self, events):
        """نظام النافذة الزمنية المنزلقة (60 ثانية) لاكتشاف الهجمات"""
        now = time.time()
        recent = [e for e in events if now - e < 60]
        score = min(len(recent) / 10.0, 1.0)
        return {"threat": score > 0.6, "score": score, "label": "CRITICAL" if score > 0.8 else "NOMINAL"}

