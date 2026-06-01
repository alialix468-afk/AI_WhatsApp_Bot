# AI WhatsApp Assistant

هذا المشروع عبارة عن بوت واتساب يعمل بالذكاء الاصطناعي، ويستخدم Gemini API لمعالجة الرسائل النصية والصوتية والصورية، و Baileys لإدارة اتصالات واتساب، و FastAPI كواجهة خلفية، بالإضافة إلى لوحة تحكم لإدارة المستخدمين والإعدادات.

## الميزات

-   **معالجة الرسائل المتعددة الوسائط**: يدعم النصوص والصوت والصور.
-   **الذكاء الاصطناعي**: يستخدم Gemini API للردود الذكية.
-   **نظام الذاكرة**: يتذكر سياق المحادثات لتحسين التفاعل.
-   **الشخصيات**: يدعم شخصيات متعددة للبوت يمكن للمستخدمين الاختيار من بينها.
-   **لوحة تحكم إدارية**: لإدارة المستخدمين والإعدادات.
-   **مكافحة البريد العشوائي**: للحد من الرسائل غير المرغوب فيها.
-   **مصادقة المستخدمين**: لوحة تحكم آمنة بكلمة مرور.

## المتطلبات

-   Docker و Docker Compose
-   حساب واتساب (للبوت)
-   مفتاح API لـ Google Gemini

## الإعداد والتشغيل

اتبع الخطوات التالية لإعداد وتشغيل المشروع:

### 1. استنساخ المستودع

```bash
git clone <رابط المستودع>
cd AI_WhatsApp_Assistant
```

### 2. إعداد ملفات البيئة

قم بإنشاء ملف `.env` في المجلد الجذر للمشروع، وقم بملئه بالمتغيرات التالية (يمكنك استخدام `.env.example` كقالب):

```env
OWNER_PHONE=+967XXXXXXXXX
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
DATABASE_URL=postgresql://whatsapp_user:whatsapp_password@db:5432/whatsapp_db
SECRET_KEY=YOUR_SECRET_KEY_FOR_DASHBOARD_AUTH
BAILEYS_SERVICE_URL=http://whatsapp_service:3000

POSTGRES_DB=whatsapp_db
POSTGRES_USER=whatsapp_user
POSTGRES_PASSWORD=whatsapp_password
```

**ملاحظات:**

-   `OWNER_PHONE`: رقم هاتف المالك (مع رمز الدولة) الذي سيتم إرسال رمز الاقتران إليه.
-   `GEMINI_API_KEY`: مفتاح API الخاص بك من Google Gemini.
-   `SECRET_KEY`: مفتاح سري قوي يستخدم لتوقيع رموز JWT للمصادقة في لوحة التحكم. قم بإنشاء مفتاح عشوائي وطويل.
-   `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`: بيانات اعتماد قاعدة بيانات PostgreSQL.

ثم قم بإنشاء ملف `.env` آخر في مجلد `whatsapp_service` وقم بملئه بالمتغيرات التالية:

```env
PORT=3000
FASTAPI_WEBHOOK_URL=http://fastapi_app:8000/webhook/whatsapp
OWNER_PHONE=+967XXXXXXXXX
```

### 3. بناء وتشغيل حاويات Docker

من المجلد الجذر للمشروع، قم بتشغيل الأمر التالي:

```bash
docker-compose up --build -d
```

سيقوم هذا الأمر ببناء صور Docker وتشغيل الخدمات في الخلفية.

### 4. الاقتران بواتساب

عند تشغيل `whatsapp_service` لأول مرة، سيقوم بإنشاء رمز اقتران. سيتم إرسال هذا الرمز إلى `OWNER_PHONE` الذي حددته في ملف `.env` الرئيسي. استخدم هذا الرمز لإقران البوت بحساب واتساب الخاص بك.

### 5. الوصول إلى لوحة التحكم

يمكنك الوصول إلى لوحة التحكم عبر المتصفح على العنوان التالي:

`http://localhost:8000/dashboard`

**بيانات اعتماد تسجيل الدخول الافتراضية:**

-   **اسم المستخدم**: `admin`
-   **كلمة المرور**: `adminpass`

**ملاحظة**: يوصى بشدة بتغيير كلمة المرور الافتراضية بعد تسجيل الدخول الأول.

## هيكل المشروع

-   `AI_WhatsApp_Assistant/`
    -   `Dockerfile`: لخدمة FastAPI.
    -   `docker-compose.yml`: لتنسيق الخدمات (FastAPI، Baileys، PostgreSQL).
    -   `main.py`: تطبيق FastAPI الرئيسي.
    -   `requirements.txt`: تبعيات Python.
    -   `.env.example`: مثال لمتغيرات البيئة.
    -   `database/`
        -   `__init__.py`: تهيئة قاعدة البيانات.
        -   `models.py`: تعريف نماذج SQLAlchemy.
    -   `dashboard/`
        -   `main.py`: مسارات لوحة التحكم.
        -   `templates/`: قوالب Jinja2 للوحة التحكم.
    -   `services/`
        -   `gemini.py`: دمج Gemini API.
        -   `voice.py`: خدمات تحويل الصوت إلى نص والعكس.
        -   `memory.py`: إدارة ذاكرة المحادثة.
        -   `personality.py`: إدارة شخصيات البوت.
        -   `security.py`: خدمات الأمن ومكافحة البريد العشوائي.
    -   `whatsapp_service/`
        -   `Dockerfile`: لخدمة Baileys Node.js.
        -   `index.js`: منطق خدمة Baileys.
        -   `package.json`: تبعيات Node.js.
        -   `.env.example`: مثال لمتغيرات البيئة لخدمة واتساب.

## المساهمة

نرحب بالمساهمات! يرجى فتح مشكلة أو طلب سحب.

## الترخيص

هذا المشروع مرخص بموجب ترخيص MIT. انظر ملف `LICENSE` لمزيد من التفاصيل.
