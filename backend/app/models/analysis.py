from datetime import datetime
from app import db

class Analysis(db.Model):
    """面试分析模型"""
    __tablename__ = 'analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interviews.id'), nullable=False)
    
    # 面部表情分析
    facial_expressions = db.Column(db.JSON)  # 存储面部表情分析结果
    emotion_scores = db.Column(db.JSON)  # 存储情绪分析分数
    
    # 语音分析
    speech_clarity = db.Column(db.Float)  # 语音清晰度
    speech_speed = db.Column(db.Float)  # 语速
    speech_volume = db.Column(db.Float)  # 音量
    speech_emotion = db.Column(db.JSON)  # 语音情绪分析
    
    # 内容分析
    content_relevance = db.Column(db.Float)  # 回答相关性
    content_completeness = db.Column(db.Float)  # 回答完整性
    content_logic = db.Column(db.Float)  # 逻辑性
    keywords_matched = db.Column(db.JSON)  # 关键词匹配
    
    # 综合评分
    overall_score = db.Column(db.Float)  # 综合得分
    feedback = db.Column(db.Text)  # 反馈建议
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    interview = db.relationship('Interview', backref=db.backref('analysis', uselist=False))
    
    def to_dict(self):
        """将分析对象转换为字典"""
        return {
            'id': self.id,
            'interview_id': self.interview_id,
            'facial_expressions': self.facial_expressions,
            'emotion_scores': self.emotion_scores,
            'speech_clarity': self.speech_clarity,
            'speech_speed': self.speech_speed,
            'speech_volume': self.speech_volume,
            'speech_emotion': self.speech_emotion,
            'content_relevance': self.content_relevance,
            'content_completeness': self.content_completeness,
            'content_logic': self.content_logic,
            'keywords_matched': self.keywords_matched,
            'overall_score': self.overall_score,
            'feedback': self.feedback,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
