import os
from datetime import timedelta
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 阿里云配置
    ALIYUN_ACCESS_KEY_ID = os.getenv('ALIYUN_ACCESS_KEY_ID')
    ALIYUN_ACCESS_KEY_SECRET = os.getenv('ALIYUN_ACCESS_KEY_SECRET')
    
    # 其他配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    
    # 讯飞API配置
    XUNFEI_APPID = 'af632c9a'
    XUNFEI_APIKEY = '0f38b7916bc3ee000443a308b1d0d8da'
    XUNFEI_APISECRET = 'ZGY3MGMyZjM1NjhjNjU3MzU3ZWQ0MDMw'

class DevelopmentConfig(Config):
    DEBUG = True
    # 使用MySQL配置，连接到main数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/dev?charset=utf8mb4'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

