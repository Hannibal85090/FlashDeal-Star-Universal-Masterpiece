"""
FlashDeal Star — Voice Parser
Parses multilingual commands: AR / FR / EN / DE / IT
"""
import re

KEYWORDS = {
    "pay":    ["ادفع","دفع","حول","أرسل","pay","send","transfer","payer","envoyer","zahlen","senden","paga","invia"],
    "buy":    ["اشتري","اشترِ","buy","acheter","kaufen","compra","comprar"],
    "cancel": ["إلغاء","ألغِ","cancel","annuler","stornieren","cancella"],
    "check":  ["تحقق","رصيد","balance","check","solde","saldo"],
}

# دعم العملات الدقيقة جداً (Nanopayments)
AMOUNTS_AR = {"ميكروسنت":0.000001, "مليسنت":0.001, "سنت":0.01, "دولار":1, "يورو":1}
CHAIN_MAP  = {
    "sei":"sei", "سي":"sei", "polygon":"polygon", "بوليغون":"polygon",
    "solana":"solana", "سولانا":"solana", "ethereum":"ethereum", "إيثيريوم":"ethereum",
    "avax":"avalanche", "avalanche":"avalanche",
}

def parse_voice_command(text: str) -> dict:
    text_l = text.lower().strip()
    intent = "unknown"
    for k, words in KEYWORDS.items():
        if any(w in text_l for w in words):
            intent = k
            break

    # استخراج المبلغ
    amount = 0.0
    m = re.search(r"(\d+(?:[.,]\d+)?)", text_l)
    if m:
        amount = float(m.group(1).replace(",", "."))
    for word, val in AMOUNTS_AR.items():
        if word in text_l:
            amount = val
            break

    # تحديد الشبكة (Blockchain)
    chain = "polygon"
    for key, val in CHAIN_MAP.items():
        if key in text_l:
            chain = val
            break

    return {"intent": intent, "amount": amount, "chain": chain, "raw": text}
