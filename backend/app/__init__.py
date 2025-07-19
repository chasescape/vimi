from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from app import config
import logging
from logging.handlers import RotatingFileHandler
import os

# 实例化扩展
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config.config[config_name])

    # 配置日志
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/vimi.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Vimi startup')

    # 配置CORS
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    with app.app_context():
        # 导入和注册蓝图
        from .routes.vision import vision_bp
        from .routes.user import user_bp
        from .routes.main import bp as main_bp
        from .routes.tts import tts_bp
        from .routes.asr import asr_bp
        from .routes.ai.spark import spark_bp
        from .routes.auth import auth_bp
        
        app.register_blueprint(asr_bp, url_prefix='/api/asr')
        app.register_blueprint(vision_bp, url_prefix='/api/vision')
        app.register_blueprint(user_bp, url_prefix='/api/user')
        app.register_blueprint(tts_bp, url_prefix='/api/tts')
        app.register_blueprint(spark_bp, url_prefix='/api/spark')
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(main_bp)
    
        # 创建数据库表
        db.create_all()
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not found',
            'message': 'The requested resource was not found'
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}')
        return jsonify({
            'error': 'Internal server error',
            'message': str(error)
        }), 500

    return app