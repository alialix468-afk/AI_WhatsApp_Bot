from sqlalchemy.orm import Session
from database.models import User, Message, Setting
from typing import List, Dict

class MemoryService:
    def __init__(self, max_messages=50):
        self.max_messages = max_messages

    def add_message(self, db: Session, user_id: int, sender: str, content: str, message_type: str):
        new_message = Message(user_id=user_id, sender=sender, content=content, message_type=message_type)
        db.add(new_message)
        db.commit()
        db.refresh(new_message)

    def get_conversation_history(self, db: Session, user_id: int) -> List[Dict]:
        messages = db.query(Message).filter(Message.user_id == user_id).order_by(Message.timestamp.desc()).limit(self.max_messages).all()
        return [{"sender": msg.sender, "text": msg.content} for msg in reversed(messages)]

    def update_preference(self, db: Session, user_id: int, key: str, value: str):
        setting = db.query(Setting).filter(Setting.user_id == user_id, Setting.key == key).first()
        if setting:
            setting.value = value
        else:
            setting = Setting(user_id=user_id, key=key, value=value)
            db.add(setting)
        db.commit()
        db.refresh(setting)

    def get_preference(self, db: Session, user_id: int, key: str, default: str = None) -> str:
        setting = db.query(Setting).filter(Setting.user_id == user_id, Setting.key == key).first()
        return setting.value if setting else default

    async def summarize_conversation(self, db: Session, user_id: int) -> str:
        history = self.get_conversation_history(db, user_id)
        if not history:
            return ""
        
        full_conversation = " ".join([f"{msg["sender"]}: {msg["text"]}" for msg in history])
        return f"ملخص المحادثة: {full_conversation[-200:]}..." # Truncate for brevity
