from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer, default=2)  # 1为面试官，2为应聘者
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # 关联
    resumes = db.relationship('Resume', back_populates='user', lazy='dynamic')
    interviews = db.relationship('Interview', back_populates='user', lazy='dynamic')
    speech_records = db.relationship('SpeechRecord', back_populates='user', lazy='dynamic')
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """将用户对象转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Resume(db.Model):
    """简历模型"""
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))
    birth_date = db.Column(db.Date)
    education = db.Column(db.String(50))  # 最高学历
    school = db.Column(db.String(100))    # 毕业院校
    major = db.Column(db.String(100))     # 专业
    experience_years = db.Column(db.Integer)  # 工作年限
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    self_introduction = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    user = db.relationship('User', back_populates='resumes')
    work_experiences = db.relationship('WorkExperience', back_populates='resume', cascade='all, delete-orphan')
    project_experiences = db.relationship('ProjectExperience', back_populates='resume', cascade='all, delete-orphan')
    education_experiences = db.relationship('EducationExperience', back_populates='resume', cascade='all, delete-orphan')
    skills = db.relationship('Skill', back_populates='resume', cascade='all, delete-orphan')

class WorkExperience(db.Model):
    """工作经历"""
    __tablename__ = 'work_experiences'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)  # 空表示至今
    description = db.Column(db.Text)
    
    resume = db.relationship('Resume', back_populates='work_experiences')

class ProjectExperience(db.Model):
    """项目经历"""
    __tablename__ = 'project_experiences'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    description = db.Column(db.Text)
    technologies = db.Column(db.String(255))  # 使用的技术栈
    
    resume = db.relationship('Resume', back_populates='project_experiences')

class EducationExperience(db.Model):
    """教育经历"""
    __tablename__ = 'education_experiences'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(100))
    degree = db.Column(db.String(50))  # 学位
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    gpa = db.Column(db.Float)
    
    resume = db.relationship('Resume', back_populates='education_experiences')

class Skill(db.Model):
    """技能"""
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer)  # 1-5 表示熟练度
    description = db.Column(db.String(255))
    
    resume = db.relationship('Resume', back_populates='skills')
    