import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # 基本配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(basedir), 'instance', 'dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or secrets.token_hex(32)
    JWT_ACCESS_TOKEN_EXPIRES = 24 * 60 * 60  # 24小时
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(basedir), 'uploads')
    
    # 阿里云配置
    ALIYUN_ACCESS_KEY_ID = 'LTAI5tRHUHUZNHGZWbVEFsVx'
    ALIYUN_ACCESS_KEY_SECRET = 'Aq5Zt0GQVWBFVDTQTGgKBGQzh6F8Fy'
    
    # 讯飞API配置
    XUNFEI_APPID = 'af632c9a'
    XUNFEI_APIKEY = '0f38b7916bc3ee000443a308b1d0d8da'
    XUNFEI_APISECRET = 'ZGY3MGMyZjM1NjhjNjU3MzU3ZWQ0MDMw'

    # OSS配置
    OSS_ENDPOINT = 'oss-cn-guangzhou.aliyuncs.com'
    OSS_BUCKET_NAME = 'vimi-save'
    OSS_ACCESS_KEY_ID = 'LTAI5tRHUHUZNHGZWbVEFsVx'
    OSS_ACCESS_KEY_SECRET = 'Aq5Zt0GQVWBFVDTQTGgKBGQzh6F8Fy'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod.db'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

