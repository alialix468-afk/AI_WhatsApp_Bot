FROM python:3.12-slim

WORKDIR /app

# تثبيت Node.js و npm
RUN apt-get update && apt-get install -y nodejs npm libpq-dev gcc

# تثبيت متطلبات البايثون
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary

# تثبيت متطلبات البوت (Node.js)
COPY whatsapp_service/package.json ./whatsapp_service/
RUN cd whatsapp_service && npm install

# نسخ باقي الملفات
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
