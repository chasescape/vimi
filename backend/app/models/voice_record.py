from app import db
from datetime import datetime

class VoiceRecord(db.Model):
    __tablename__ = 'voice_records'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    transcription = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sentiment = db.Column(db.Text)  # 新增，用来存情绪 JSON