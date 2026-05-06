from cryptography.fernet import Fernet

class DataVault:
    def __init__(self, key=None):
        # استباق فقدان المفتاح بتوليد واحد افتراضي آمن
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)
        
    def seal(self, plain_text):
        try:
            return self.cipher.encrypt(plain_text.encode())
        except Exception:
            return None
        
    def open(self, encrypted_data):
        try:
            return self.cipher.decrypt(encrypted_data).decode()
        except Exception:
            return "DECRYPTION_FAILED"
