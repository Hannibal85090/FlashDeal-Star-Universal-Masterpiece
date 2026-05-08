import re

KEYWORDS = {
    "pay": ["ادفع", "حول", "أرسل", "pay", "send"],
    "check": ["تحقق", "رصيد", "balance"]
}

def parse_voice_command(text):
    text_l = text.lower().strip()
    intent = "unknown"
    for k, words in KEYWORDS.items():
        if any(w in text_l for w in words):
            intent = k
            break
    
    amount = 0.0
    m = re.search(r"(\d+(?:[.,]\d+)?)", text_l)
    if m: amount = float(m.group(1))
    
    return {"intent": intent, "amount": amount, "status": "parsed"}

