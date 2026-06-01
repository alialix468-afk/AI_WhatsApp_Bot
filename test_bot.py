import asyncio
import os
from services.gemini import GeminiService
from services.voice import VoiceService
from services.personality import PersonalityService
from services.security import AntiSpamService

async def test_gemini():
    print("Testing Gemini API...")
    gemini = GeminiService()
    try:
        response = await gemini.generate_response("مرحباً، كيف حالك؟")
        print(f"Gemini Response: {response}")
    except Exception as e:
        print(f"Gemini Error: {e}")

async def test_voice():
    print("\nTesting Voice Service...")
    voice = VoiceService()
    try:
        # Testing TTS
        audio_bytes = await voice.text_to_speech("مرحباً بك في بوت الواتساب الذكي.")
        print(f"TTS generated {len(audio_bytes)} bytes.")
    except Exception as e:
        print(f"Voice Error: {e}")

async def test_personality():
    print("\nTesting Personality Service...")
    personality = PersonalityService()
    personalities = personality.list_personalities()
    print(f"Available Personalities: {list(personalities.keys())}")
    friendly_prompt = personality.get_personality_prompt("friendly")
    print(f"Friendly Prompt (truncated): {friendly_prompt[:50]}...")

async def test_antispam():
    print("\nTesting AntiSpam Service...")
    antispam = AntiSpamService(max_messages_per_minute=2)
    user_id = "test_user"
    print(f"Request 1: {antispam.is_spam(user_id)}") # False
    print(f"Request 2: {antispam.is_spam(user_id)}") # False
    print(f"Request 3: {antispam.is_spam(user_id)}") # True
    print(f"Request 4: {antispam.is_spam(user_id)}") # True

async def main():
    # Set mock environment variables for testing
    os.environ["GEMINI_API_KEY"] = "test_key"
    
    await test_gemini()
    await test_voice()
    await test_personality()
    await test_antispam()

if __name__ == "__main__":
    asyncio.run(main())
