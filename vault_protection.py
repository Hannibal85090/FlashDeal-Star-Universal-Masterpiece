"""
FlashDeal Star — Data Vault
"""
import hashlib, json, time

class DataVault:
    def __init__(self):
        self._store = {}
    
    def store(self, key, value, secret="sovereign"):
        dk = hashlib.sha256(secret.encode()).hexdigest()
        self._store[key] = json.dumps({"data": value, "hash": dk[:8]})
        return True

    def retrieve(self, key, secret="sovereign"):
        raw = self._store.get(key)
        if not raw: return None
        obj = json.loads(raw)
        if obj["hash"] != hashlib.sha256(secret.encode()).hexdigest()[:8]:
            return None
        return obj["data"]

