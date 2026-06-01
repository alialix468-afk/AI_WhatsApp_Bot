from fastapi import FastAPI, Request
import requests, subprocess, edge_tts, os

app = FastAPI()
API_KEY = ""
VOICE = "ar-XA-ElenaNeural"
# المسار المطلق للوصول للملف من أي مكان
BASE_PATH = "/data/data/com.termux/files/home/AI_WhatsApp_Assistant"

@app.post("/webhook")
async def handle_message(request: Request):
    data = await request.json()
    user_id = data.get("sender", "user")
    message = data.get("message", "")
    msg_type = data.get("type", "text")
    
    # الرد (نفس المنطق السابق)
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": "أنت 'بلك هوت' الصنعاني، رد بلهجة صنعانية عفوية."}, {"role": "user", "content": message}]}
    
    try:
        r = requests.post(url, headers=headers, json=payload)
        reply_text = r.json()['choices'][0]['message']['content']
    except Exception as e:
        return {"reply": "عفواً، صار خطأ في التواصل مع العقل!"}
    
    audio_path = os.path.join(BASE_PATH, "voice_response.ogg")
    
    if msg_type == "voice":
        try:
            communicate = edge_tts.Communicate(reply_text, VOICE)
            await communicate.save(os.path.join(BASE_PATH, "temp.mp3"))
            # تأكد أن ffmpeg موجود في المسار
            subprocess.run(["ffmpeg", "-y", "-i", os.path.join(BASE_PATH, "temp.mp3"), "-c:a", "libopus", audio_path], check=True)
            return {"reply": reply_text, "audio": audio_path}
        except Exception as e:
            # هنا ستعرف السبب لو فشل الصوت!
            return {"reply": f"فشل الصوت: {str(e)}"}
    
    return {"reply": reply_text}

