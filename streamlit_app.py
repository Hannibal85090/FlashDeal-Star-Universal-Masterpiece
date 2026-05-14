import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import requests
import datetime
import hashlib
import time
from loguru import logger
import os

# --------------------- الإعدادات ---------------------
st.set_page_config(
    page_title=" FlashDeal Star",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------- الثوابت ---------------------
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")
SECRET_KEY = os.getenv("SECRET_KEY", "flashdeal-secret-key")
TOKEN_EXPIRE_MINUTES = 15

# --------------------- وظائف المساعدة ---------------------
def generate_sovereign_hash(timestamp: str) -> str:
    return hashlib.sha256(f"{SECRET_KEY}{timestamp}".encode()).hexdigest()

def process_payment(method: str, metadata: dict) -> dict:
    timestamp = datetime.datetime.now().isoformat()
    sovereign_hash = generate_sovereign_hash(timestamp)
    
    payload = {
        "method": method,
        "metadata": metadata,
        "hash": sovereign_hash,
        "timestamp": timestamp
    }
    
    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token', '')}"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/payment",
            json=payload,
            headers=headers,
            timeout=10
        )
        return response.json()
    except Exception as e:
        logger.error(f"Payment API Error: {e}")
        return {"status": "error", "message": str(e)}

# --------------------- واجهة المستخدم ---------------------
st.title(" FlashDeal Star - Sovereign Pay")
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab
