"""
FlashDeal Star — Data Vault
Lightweight encrypted key-value store (no external crypto deps required for demo)
"""
import hashlib, json, os, time

class DataVault:
    def __init__(self, vault_id: str = "flashdeal_main"):
        self.vault_id  = vault_id
        self._store    = {}
        self._audit    = []

    def _derive_key(self, secret: str) -> str:
        return hashlib.sha256(secret.encode()).hexdigest()

    def store(self, key: str, value: dict, secret: str = "sovereign") -> bool:
        dk = self._derive_key(secret)
        payload = json.dumps({"data": value, "ts": int(time.time()), "key_hash": dk[:8]})
        self._store[key] = payload
        self._audit.append({"action": "WRITE", "key": key, "ts": int(time.time())})
        return True

    def retrieve(self, key: str, secret: str = "sovereign") -> dict | None:
        raw = self._store.get(key)
        if not raw:
            return None
        obj = json.loads(raw)
        dk  = self._derive_key(secret)
        if obj.get("key_hash") != dk[:8]:
            return None
        self._audit.append({"action": "READ", "key": key, "ts": int(time.time())})
        return obj["data"]

    def audit_log(self) -> list:
        return self._audit[-20:]

    def wipe(self, secret: str = "sovereign") -> bool:
        self._store.clear()
        self._audit.append({"action": "WIPE", "ts": int(time.time())})
        return True

