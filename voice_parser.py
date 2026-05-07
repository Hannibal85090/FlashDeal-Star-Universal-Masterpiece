"""
FlashDeal Star â€” Voice Parser
Parses multilingual commands: AR / FR / EN / DE / IT
"""
import re

KEYWORDS = {
    "pay":    ["ط§ط¯ظپط¹","ط¯ظپط¹","ط­ظˆظ„","ط£ط±ط³ظ„","pay","send","transfer","payer","envoyer","zahlen","senden","paga","invia"],
    "buy":    ["ط§ط´طھط±ظٹ","ط§ط´طھط±ظگ","buy","acheter","kaufen","compra","comprar"],
    "cancel": ["ط¥ظ„ط؛ط§ط،","ط£ظ„ط؛ظگ","cancel","annuler","stornieren","cancella"],
    "check":  ["طھط­ظ‚ظ‚","ط±طµظٹط¯","balance","check","solde","saldo"],
}

AMOUNTS_AR = {"ظ…ظٹظƒط±ظˆط³ظ†طھ":0.000001,"ظ…ظ„ظٹط³ظ†طھ":0.001,"ط³ظ†طھ":0.01,"ط¯ظˆظ„ط§ط±":1,"ظٹظˆط±ظˆ":1}
CHAIN_MAP  = {
    "sei":"sei","ط³ظٹ":"sei","polygon":"polygon","ط¨ظˆظ„ظٹط؛ظˆظ†":"polygon",
    "solana":"solana","ط³ظˆظ„ط§ظ†ط§":"solana","ethereum":"ethereum","ط¥ظٹط«ظٹط±ظٹظˆظ…":"ethereum",
    "avax":"avalanche","avalanche":"avalanche",
}

def parse_voice_command(text: str) -> dict:
    text_l = text.lower().strip()
    intent = "unknown"
    for k, words in KEYWORDS.items():
        if any(w in text_l for w in words):
            intent = k
            break

    # amount extraction
    amount = 0.0
    m = re.search(r"(\d+(?:[.,]\d+)?)", text_l)
    if m:
        amount = float(m.group(1).replace(",", "."))
    for word, val in AMOUNTS_AR.items():
        if word in text_l:
            amount = val
            break

    # chain extraction
    chain = "polygon"
    for key, val in CHAIN_MAP.items():
        if key in text_l:
            chain = val
            break

    # destination
    dest_match = re.search(r"0x[0-9a-fA-F]{8,}", text)
    destination = dest_match.group(0) if dest_match else "0x_FLASHDEAL_VAULT"

    status = "active" if intent in ("pay","buy","transfer") else "query"
    return {
        "status":      status,
        "intent":      intent,
        "amount":      amount if amount else 0.000042,
        "chain":       chain,
        "destination": destination,
        "raw":         text,
    }
