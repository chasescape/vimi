from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

# 实例化扩展

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO()

def create_app(config_name='development'):
    app = Flask(__name__)
    # 正确加载类配置
    from .config import config
    app.config.from_object(config[config_name])

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # 这里可以注册蓝图
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app 