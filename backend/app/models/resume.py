from datetime import datetime
from app import db

class Resume(db.Model):
    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    # 简历内容
    basic_info = db.Column(db.JSON, nullable=False)  # 基本信息
    education = db.Column(db.JSON)  # 教育经历
    work_experience = db.Column(db.JSON)  # 工作经历
    projects = db.Column(db.JSON)  # 项目经历
    skills = db.Column(db.JSON)  # 技能标签
    
    # 文件相关
    file_url = db.Column(db.String(255))  # 上传的简历文件URL
    
    # 统计信息
    completion_score = db.Column(db.Integer, default=0)  # 完整度评分
    applied_jobs = db.Column(db.Integer, default=0)  # 已投递职位数
    
    # 分享相关
    share_code = db.Column(db.String(50), unique=True)  # 分享码
    share_expire_time = db.Column(db.DateTime)  # 分享过期时间
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    work_experiences = db.relationship('WorkExperience', back_populates='resume', cascade='all, delete-orphan')
    project_experiences = db.relationship('ProjectExperience', back_populates='resume', cascade='all, delete-orphan')
    education_experiences = db.relationship('EducationExperience', back_populates='resume', cascade='all, delete-orphan')
    skills = db.relationship('Skill', back_populates='resume', cascade='all, delete-orphan')

    def __init__(self, user_id, name, basic_info):
        self.user_id = user_id
        self.name = name
        self.basic_info = basic_info
        self.education = []
        self.work_experience = []
        self.projects = []
        self.skills = []

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'basic_info': self.basic_info,
            'education': self.education,
            'work_experience': self.work_experience,
            'projects': self.projects,
            'skills': self.skills,
            'file_url': self.file_url,
            'completion_score': self.completion_score,
            'applied_jobs': self.applied_jobs,
            'share_code': self.share_code,
            'share_expire_time': self.share_expire_time.strftime('%Y-%m-%d %H:%M:%S') if self.share_expire_time else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def calculate_completion_score(self):
        score = 0
        total = 5  # 总评分项：基本信息、教育经历、工作经历、项目经历、技能特长
        
        if self.basic_info and all(self.basic_info.get(k) for k in ['name', 'phone', 'email']):
            score += 1
        if self.education and len(self.education) > 0:
            score += 1
        if self.work_experience and len(self.work_experience) > 0:
            score += 1
        if self.projects and len(self.projects) > 0:
            score += 1
        if self.skills and len(self.skills) > 0:
            score += 1
            
        self.completion_score = int((score / total) * 100)
        return self.completion_score

    def is_share_valid(self):
        """检查分享链接是否有效"""
        if not self.share_code or not self.share_expire_time:
            return False
        return datetime.utcnow().timestamp() < self.share_expire_time.timestamp()

    @classmethod
    def get_by_share_code(cls, share_code):
        """通过分享码获取简历"""
        return cls.query.filter_by(share_code=share_code).first()

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