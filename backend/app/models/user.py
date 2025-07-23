from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # 添加邮箱字段
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='candidate')
    
    # 个人信息
    avatar = db.Column(db.String(255))
    name = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    birthday = db.Column(db.Date)
    phone = db.Column(db.String(20))
    location = db.Column(db.JSON)  # {province: '', city: ''}
    
    # 账号设置
    linkedin_bound = db.Column(db.Boolean, default=False)
    email_notification = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)  # 邮箱是否已验证
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    resumes = db.relationship('Resume', backref='user', lazy=True)
    applications = db.relationship('JobApplication', backref='user', lazy=True)

    def __init__(self, username, password, email, role='candidate'):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'avatar': self.avatar,
            'name': self.name,
            'gender': self.gender,
            'birthday': self.birthday.strftime('%Y-%m-%d') if self.birthday else None,
            'phone': self.phone,
            'location': self.location,
            'linkedin_bound': self.linkedin_bound,
            'email_notification': self.email_notification,
            'email_verified': self.email_verified,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    