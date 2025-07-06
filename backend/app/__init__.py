from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from app import config

# 实例化扩展
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO()

def create_app(config_name='default'):
    app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
    app.config.from_object(config.config[config_name])

    # 配置CORS
    CORS(app, 
        resources={
            r"/*": {  # 允许所有路由
                "origins": [
                    "http://localhost:5173",  # Vite 开发服务器
                    "http://localhost:3000",  # 其他可能的前端开发服务器
                    "http://127.0.0.1:5173",  # 使用 IP 地址访问
                    "http://localhost:8080"   # Vue CLI 开发服务器
                ],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
                "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "Accept"],
                "expose_headers": ["Content-Length", "Content-Range"],
                "supports_credentials": True,
                "max_age": 86400  # 预检请求的缓存时间（24小时）
            }
        }
    )

    # 添加CORS预检请求处理
    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        if origin and origin in [
            "http://localhost:5173",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
            "http://localhost:8080"
        ]:
            # 即使是错误响应也添加CORS头部
            response.headers.add('Access-Control-Allow-Origin', origin)
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With,Accept')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Max-Age', '86400')
            
            # 确保错误响应也返回正确的Content-Type
            if response.status_code >= 400:
                response.headers['Content-Type'] = 'application/json'
        return response

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    with app.app_context():
        # 导入和注册蓝图
        from .routes.vision import vision_bp
        from .routes.user import user_bp
        from .routes import main

        app.register_blueprint(vision_bp, url_prefix='/api/vision')
        app.register_blueprint(user_bp, url_prefix='/api/user')
        app.register_blueprint(main.bp)

    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not found',
            'message': 'The requested resource was not found'
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal server error',
            'message': str(error)
        }), 500

    return app 