from datetime import datetime
from app import db
from sqlalchemy import Column, Text
class JobApplication(db.Model):
    __tablename__ = 'job_applications'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 申请人
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)    # 岗位ID

    apply_time = db.Column(db.DateTime, default=datetime.utcnow)  # 申请时间

    # 状态：待审核、通过、拒绝
    status = db.Column(db.String(20), default='待审核')
    resume_path = db.Column(db.String(255))  # ✅ 简历文件路径（可选）
    interview_time = db.Column(db.DateTime, nullable=True)  # ✅ 面试时间（可选）
    interview_link = db.Column(db.String(255))  # ✅ 面试链接（可选
    # 关系映射（可选，方便 ORM 查询）
    user = db.relationship('User', backref='applications')
    job = db.relationship('Job', backref='applications')
    photo_path = db.Column(db.String(255))  # 新增：照片文件路径（可选）
    audio_path = db.Column(db.String(255))  # ✅ 新增：面试语音文件 URL
    evaluation_result = db.Column(Text, nullable=True)