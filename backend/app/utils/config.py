import os

# 讯飞API配置
XUNFEI_CONFIG = {
    'APP_ID': 'af632c9a',
    'API_KEY': '0f38b7916bc3ee000443a308b1d0d8da',
    'API_SECRET': 'ZGY3MGMyZjM1NjhjNjU3MzU3ZWQ0MDMw',
    'FACE_API_URL': 'https://api.xf-yun.com/v1/private/s67c9c78c'
}
# 数据库配置
DATABASE_CONFIG = {
    'TYPE': 'mysql',
    'HOST': 'localhost',
    'PORT': 3306,
    'NAME': 'vimi',
    'USER': 'root',
    'PASSWORD': '123456'
}

# Flask应用配置
FLASK_CONFIG = {
    'SECRET_KEY': 'dev',
    'DEBUG': True
}