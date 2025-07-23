from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from .config import config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # 启用CORS，允许所有源
    CORS(app, supports_credentials=True)
    
    # 注册蓝图
    from .routes.auth import auth_bp
    from .routes.resume import resume_bp
    from .routes.job import job_bp
    from .routes.interview import interview_bp
    from .routes.user import user_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(resume_bp, url_prefix='/api/resume')
    app.register_blueprint(job_bp, url_prefix='/api/job')
    app.register_blueprint(interview_bp, url_prefix='/api/interview')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    
    return app