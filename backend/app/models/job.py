from app import db
from datetime import datetime

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_category = db.Column(db.String(50))
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    salary_type = db.Column(db.String(10))
    experience_req = db.Column(db.String(50))
    education_req = db.Column(db.String(50))
    location = db.Column(db.String(100))
    job_nature = db.Column(db.String(20))
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)
    benefits = db.Column(db.Text)
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    expire_date = db.Column(db.DateTime)
    view_count = db.Column(db.Integer, default=0)
    apply_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='发布')
    contact_email = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))
    address_detail = db.Column(db.String(200))
