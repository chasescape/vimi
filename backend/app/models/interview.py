from datetime import datetime
from app import db

class Interview(db.Model):
    __tablename__ = 'interviews'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('job_applications.id'))
    interviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    candidate_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 面试信息
    schedule_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # 面试时长（分钟）
    status = db.Column(db.String(20), default='scheduled')  # scheduled, ongoing, completed, cancelled
    interview_type = db.Column(db.String(20), nullable=False)  # online, offline, ai
    
    # 面试详情
    meeting_link = db.Column(db.String(255))  # 在线面试链接
    location = db.Column(db.Text)  # 线下面试地点
    notes = db.Column(db.Text)  # 面试备注
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    evaluation = db.relationship('InterviewEvaluation', backref='interview', lazy=True, uselist=False)
    questions = db.relationship('Question', backref='interview', lazy=True)
    answers = db.relationship('Answer', backref='interview', lazy=True)
    interviewer = db.relationship('User', foreign_keys=[interviewer_id], backref='interviews_as_interviewer')
    candidate = db.relationship('User', foreign_keys=[candidate_id], backref='interviews_as_candidate')

    def to_dict(self):
        return {
            'id': self.id,
            'application_id': self.application_id,
            'interviewer_id': self.interviewer_id,
            'candidate_id': self.candidate_id,
            'schedule_time': self.schedule_time.strftime('%Y-%m-%d %H:%M:%S'),
            'duration': self.duration,
            'status': self.status,
            'interview_type': self.interview_type,
            'meeting_link': self.meeting_link,
            'location': self.location,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'evaluation': self.evaluation.to_dict() if self.evaluation else None
        }

class Question(db.Model):
    """面试问题模型"""
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interviews.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)  # 问题内容
    tips = db.Column(db.Text)  # 问题提示
    difficulty = db.Column(db.String(20))  # 难度：easy, medium, hard
    category = db.Column(db.String(50))  # 问题类别：technical, behavioral, etc.
    order = db.Column(db.Integer)  # 问题顺序
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    answers = db.relationship('Answer', backref='question', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'interview_id': self.interview_id,
            'content': self.content,
            'tips': self.tips,
            'difficulty': self.difficulty,
            'category': self.category,
            'order': self.order,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Answer(db.Model):
    """面试答案模型"""
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interviews.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)  # 答案内容
    duration = db.Column(db.Integer)  # 回答用时（秒）
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 评估信息
    score = db.Column(db.Float)  # 得分
    feedback = db.Column(db.Text)  # 反馈
    keywords_matched = db.Column(db.JSON)  # 匹配到的关键词

    def to_dict(self):
        return {
            'id': self.id,
            'interview_id': self.interview_id,
            'question_id': self.question_id,
            'content': self.content,
            'duration': self.duration,
            'score': self.score,
            'feedback': self.feedback,
            'keywords_matched': self.keywords_matched,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class InterviewEvaluation(db.Model):
    __tablename__ = 'interview_evaluations'

    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interviews.id'), nullable=False)
    
    # 评分
    overall_rating = db.Column(db.Integer)  # 总体评分
    technical_rating = db.Column(db.Integer)  # 技术评分
    communication_rating = db.Column(db.Integer)  # 沟通评分
    experience_rating = db.Column(db.Integer)  # 经验评分
    culture_fit_rating = db.Column(db.Integer)  # 文化匹配评分
    
    # 评价
    strengths = db.Column(db.JSON)  # 优势列表
    weaknesses = db.Column(db.JSON)  # 待改进列表
    feedback = db.Column(db.Text)  # 详细反馈
    recommendation = db.Column(db.String(20))  # hire, reject, consider
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'interview_id': self.interview_id,
            'overall_rating': self.overall_rating,
            'technical_rating': self.technical_rating,
            'communication_rating': self.communication_rating,
            'experience_rating': self.experience_rating,
            'culture_fit_rating': self.culture_fit_rating,
            'strengths': self.strengths,
            'weaknesses': self.weaknesses,
            'feedback': self.feedback,
            'recommendation': self.recommendation,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class AIInterviewRecord(db.Model):
    __tablename__ = 'ai_interview_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 面试设置
    position = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # 面试时长（分钟）
    difficulty = db.Column(db.Integer, nullable=False)  # 面试难度 1-3
    
    # 面试记录
    questions = db.Column(db.JSON)  # 面试问题及回答
    video_url = db.Column(db.String(255))  # 面试视频记录
    score = db.Column(db.Integer)  # 面试得分
    feedback = db.Column(db.Text)  # AI反馈
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'position': self.position,
            'duration': self.duration,
            'difficulty': self.difficulty,
            'questions': self.questions,
            'video_url': self.video_url,
            'score': self.score,
            'feedback': self.feedback,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } 