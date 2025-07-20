from datetime import datetime
from app import db

class Interview(db.Model):
    """面试模型"""
    __tablename__ = 'interviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, ongoing, completed
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    score = db.Column(db.Float)
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    user = db.relationship('User', back_populates='interviews')
    
    def to_dict(self):
        """将面试对象转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'status': self.status,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'score': self.score,
            'feedback': self.feedback,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 