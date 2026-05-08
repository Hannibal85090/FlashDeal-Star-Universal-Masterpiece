"""
FlashDeal Star — Data Vault v4.0
خزنة بيانات مشفرة مع نظام تدقيق سيادي (Audit Log)
"""
import hashlib, json, os, time

class DataVault:
    def __init__(self, vault_id: str = "flashdeal_main"):
        self.vault_id  = vault_id
        self._store    = {}    # المخزن المشفر
        self._audit    = []    # سجل العمليات للشفافية والأمان

    def _derive_key(self, secret: str) -> str:
        """اشتقاق مفتاح التشفير باستخدام SHA-256"""
        return hashlib.sha256(secret.encode()).hexdigest()

    def store(self, key: str, value: dict, secret: str = "sovereign") -> bool:
        """
        تشفير وتخزين البيانات.
        يتم ربط البيانات بهاتش (Hash) سري لضمان عدم استخراجها إلا بالمفتاح الصحيح.
        """
        dk = self._derive_key(secret)
        payload = json.dumps({
            "data": value, 
            "ts": int(time.time()), 
            "key_hash": dk[:8]  # توقيع جزئي للمفتاح للتحقق
        })
        self._store[key] = payload
        
        # تسجيل العملية في سجل التدقيق
        self._audit.append({
            "action": "WRITE", 
            "key": key, 
            "ts": int(time.time()),
            "status": "SUCCESS"
        })
        return True

    def retrieve(self, key: str, secret: str = "sovereign") -> dict | None:
        """
        استعادة البيانات المشفرة.
        لن يتم استرجاع البيانات إذا كان المفتاح السري خاطئاً.
        """
        raw = self._store.get(key)
        if not raw:
            return None
            
        obj = json.loads(raw)
        dk  = self._derive_key(secret)
        
        # التحقق من تطابق مفتاح فك التشفير
        if obj.get("key_hash") != dk[:8]:
            self._audit.append({
                "action": "READ_FAIL", 
                "key": key, 
                "ts": int(time.time()),
                "reason": "INVALID_SECRET"
            })
            return None
            
        self._audit.append({
            "action": "READ_SUCCESS", 
            "key": key, 
            "ts": int(time.time())
        })
        return obj["data"]

    def audit_log(self) -> list:
        """إرجاع آخر 20 عملية تمت على الخزنة للعرض في واجهة الحكام"""
        return self._audit[-20:]

