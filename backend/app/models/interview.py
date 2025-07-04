from app import db
from datetime import datetime

class Interview(db.Model):
    __tablename__ = 'interviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending')
    score = db.Column(db.Float)
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # 关联关系
    questions = db.relationship('InterviewQuestion', backref='interview', lazy=True)
    user = db.relationship('User', backref='interviews')

class InterviewQuestion(db.Model):
    __tablename__ = 'interview_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interviews.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text)
    score = db.Column(db.Float)
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 