FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y nodejs npm libpq-dev gcc
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary
COPY whatsapp_service/package.json ./whatsapp_service/
RUN cd whatsapp_service && npm install
COPY . .
RUN chmod +x start.sh
CMD ["./start.sh"]
