import re

def parse_voice_command(text_input):
    # استباق أخطاء النصوص الفارغة (Input Validation)
    if not text_input or not isinstance(text_input, str):
        return {"status": "void", "action": None, "amount": 0.0}
    
    clean_text = text_input.lower().strip()
    result = {"status": "unrecognized", "action": None, "amount": 0.0}

    # التثبت من الكلمة المفتاحية (Keyword Guard)
    if "flashdeal star" in clean_text:
        result["status"] = "active"
        if "pay" in clean_text:
            result["action"] = "payment"
            # استخراج الأرقام بدقة (Integer & Float Support)
            matches = re.findall(r'\d+(?:\.\d+)?', clean_text)
            if matches:
                result["amount"] = float(matches[0])
    return result

