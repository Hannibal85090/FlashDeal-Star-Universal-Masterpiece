import subprocess
import sys
import os

# --- إعدادات الألوان للوضوح البصري ---
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

# --- القاعدة الذهبية: التحقق من إصدار بايثون ---
if sys.version_info < (3, 8):
    print(f"{RED}{BOLD}❌ خطأ: يتطلب مشروع My FlashDeal Star إصدار Python 3.8 أو أعلى.{RESET}")
    print(f"{YELLOW}الإصدار الحالي لديك هو: {sys.version.split()[0]}{RESET}")
    sys.exit(1)

def install_package(name, args):
    """دالة احترافية لتثبيت المجموعات مع التحقق من وجود الملف"""
    if not os.path.exists(args[1]):
        print(f"{RED}❌ خطأ: لم يتم العثور على ملف {args[1]}{RESET}")
        return False
    
    print(f"{YELLOW}⏳ جاري تثبيت {name}...{RESET}")
    try:
        # استخدام --upgrade لضمان استقرار النسخ المحددة
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade"] + args)
        print(f"{GREEN}✅ اكتمل تثبيت {name} بنجاح.{RESET}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{RED}❌ فشل تثبيت {name}: {e}{RESET}")
        return False

def main():
    print(f"\n{BOLD}{YELLOW}🌟 FlashDeal Star Universal: نظام التثبيت الذكي 🌟{RESET}")
    print(f"{YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")
    
    # 1. تحديث أداة Pip أولاً لضمان أفضل توافق
    print(f"{YELLOW}🛠️ الخطوة 0: تحديث أداة Pip...{RESET}")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print(f"{GREEN}✅ أداة Pip محدثة وجاهزة.{RESET}\n")
    except Exception as e:
        print(f"{RED}⚠️ تحذير: فشل تحديث Pip، سنحاول الاستمرار: {e}{RESET}\n")

    # 2. تثبيت الأساسيات (base.txt)
    success_base = install_package("الأساسيات (Base Core)", ["-r", "requirements/base.txt"])
    
    # 3. تثبيت محرك لغة الإشارة (اختياري عبر Flag)
    if success_base and "--with-sign" in sys.argv:
        print(f"\n{YELLOW}🧠 جاري تجهيز محركات الذكاء الاصطناعي...{RESET}")
        install_package("لغة الإشارة (Sign Language)", ["-r", "requirements/sign_language.txt"])
    
    # 4. رسالة توجيهية
    elif success_base:
        print(f"\n{YELLOW}💡 نصيحة: لتشغيل قدرات لغة الإشارة لاحقاً، استخدم:{RESET}")
        print(f"{BOLD}python install.py --with-sign{RESET}")

    print(f"\n{GREEN}{BOLD}🏁 النتيجة: بيئة العمل جاهزة تماماً. نجمك الآن في أبهى حلة!{RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}🛑 تم إيقاف العملية يدوياً.{RESET}")
        sys.exit(1)
