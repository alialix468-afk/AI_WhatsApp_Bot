from typing import Dict

class PersonalityService:
    def __init__(self):
        self.personalities: Dict[str, str] = {
            "friendly": "أنت مساعد ودود ومفيد.",
            "professional": "أنت مساعد احترافي ودقيق.",
            "funny": "أنت مساعد مرح وتحب المزاح.",
            "short": "أنت مساعد موجز ومباشر في ردودك."
        }
        self.default_personality = "friendly"

    def get_personality_prompt(self, personality_name: str) -> str:
        return self.personalities.get(personality_name, self.personalities[self.default_personality])

    def add_personality(self, name: str, prompt: str):
        self.personalities[name] = prompt

    def list_personalities(self) -> Dict[str, str]:
        return self.personalities
