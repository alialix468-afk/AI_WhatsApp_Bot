#!/bin/bash
# تشغيل البوت في الخلفية
nodejs whatsapp_service/index.js &
# تشغيل خادم الـ API
uvicorn main:app --host 0.0.0.0 --port 8000
