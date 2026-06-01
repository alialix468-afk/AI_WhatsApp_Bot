import httpx

class GeminiService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.system_prompt = """
        أنت مساعد واتساب صنعاني. مهمتك هي مساعدة المستخدمين بلهجة صنعانية يمانية دارجة ومحببة.
        - استخدم الكلمات الصنعانية الدارجة مثل: "هيا"، "يا واد"، "ما بش"، "ايش عاد"، "حيا بك"، "أبشر"، "من عيوني"، "ايش تشتي".
        - تجنب العربية الفصحى تماماً، تحدث وكأنك صديق جالس في ديوان.
        - كن ودوداً، مرحاً، ومباشراً.
        """

    async def generate_content(self, prompt: str) -> str:
        url = f"{self.base_url}?key={self.api_key}"
        payload = {
            "system_instruction": {
                "parts": [{"text": self.system_prompt}]
            },
            "contents": [{"parts": [{"text": prompt}]}]
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                return f"حدث خطأ يا غالي: {str(e)}"

