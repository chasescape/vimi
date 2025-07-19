import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
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

