from datetime import datetime
from app import db

class SpeechRecord(db.Model):
    """语音记录模型"""
    __tablename__ = 'speech_records'
    
    id = db.Column(db.Integer, primary_key=True)
    audio_file = db.Column(db.String(500), nullable=False)
    recognized_text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联
    user = db.relationship('User', back_populates='speech_records')
    
    def to_dict(self):
        """将语音记录对象转换为字典"""
        return {
            'id': self.id,
            'audio_file': self.audio_file,
            'recognized_text': self.recognized_text,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat()
        } 