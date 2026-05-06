import streamlit as st
# استيراد الوحدات مع التثبت من وجودها
try:
    from voice_parser import parse_voice_command
    from security_engine import FlashDealTokenEngine
    from vault_protection import DataVault
except ImportError as e:
    st.error(f"Missing Core Module: {e}")

def main():
    st.set_page_config(page_title="FlashDeal Star Universal", page_icon="⭐")
    st.title("🛡️ FlashDeal Star Universal")
    st.subheader("Talk. Pay. Done.")

    # منع الانهيار عند تحديث الصفحة (State Management)
    if 'processing' not in st.session_state:
        st.session_state.processing = False

    # واجهة الإدخال
    user_input = st.text_input("Enter Voice Command (Simulation):", 
                               placeholder="e.g., FlashDeal Star pay 250 USDC")

    if st.button("Execute Secure Protocol"):
        if user_input:
            st.session_state.processing = True
            try:
                # 1. المنهجية البرمجية: التحليل
                cmd = parse_voice_command(user_input)
                
                if cmd["status"] == "active" and cmd["action"] == "payment":
                    with st.status("Initiating Sovereign Protocol...", expanded=True) as status:
                        # 2. توليد التوكن التبادلي (Mutual Token)
                        engine = FlashDealTokenEngine()
                        auth = engine.generate_mutual_token("ALi_Arfaoui", "bio_hash_master")
                        
                        # 3. تشفير العملية وحفظها
                        vault = DataVault()
                        receipt_data = f"AMT:{cmd['amount']}|TKN:{auth['token'][:10]}"
                        encrypted_receipt = vault.seal(receipt_data)
                        
                        status.update(label="Transaction Secured!", state="complete", expanded=False)

                    # عرض النتائج النهائية (The Success State)
                    st.success(f"✅ Payment Authorized: {cmd['amount']} USDC")
                    st.info(f"Mutual Token: {auth['token']}")
                    st.balloons()
                else:
                    st.warning("Keyword 'FlashDeal Star' not detected. Access Denied.")
            
            except Exception as e:
                # استباق تاريخ أخطاء البرمجة: معالج الأخطاء الشامل (The Global Catch)
                st.error("A critical recovery event was handled. System is stable.")
                st.write(f"Internal Log: {str(e)}")
            finally:
                st.session_state.processing = False
        else:
            st.error("No input detected. System idling.")

if __name__ == "__main__":
    main()

