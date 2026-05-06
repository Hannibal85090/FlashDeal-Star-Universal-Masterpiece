"""FlashDeal Star — Central Configuration"""
import os

# ── API Keys (set in .env or Streamlit Secrets) ──────────────────────────────
ALSA_API_KEY    = os.getenv("ALSA_API_KEY", "")
ALSA_BASE_URL   = "https://api.aisa.one/v1"          # aisa.one endpoint
GOOGLE_API_KEY  = os.getenv("GOOGLE_API_KEY", "")
CIRCLE_API_KEY  = os.getenv("CIRCLE_API_KEY", "")

# ── App Meta ──────────────────────────────────────────────────────────────────
APP_TITLE       = "⭐ FlashDeal Star ⭐"
APP_VERSION     = "V3.0 Universal"
AUTHOR          = "Ali Arfaoui — Hannibal85090"
SLOGAN          = "Talk. Pay. Done. | تحدث. ادفع. تم."

# ── Payment ───────────────────────────────────────────────────────────────────
SUPPORTED_CHAINS = ["polygon", "sei", "ethereum", "solana", "avalanche", "base"]
MIN_AMOUNT       = 0.000001
DEFAULT_CHAIN    = "polygon"
MASTER_KEY       = os.getenv("MASTER_KEY", "sovereign_master_key_change_in_prod")

# ── Security ──────────────────────────────────────────────────────────────────
TOKEN_TTL        = 300          # seconds
ANOMALY_WINDOW   = 60           # seconds per window
MAX_TX_PER_MIN   = 10

