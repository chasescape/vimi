import os
from dotenv import load_dotenv
# 加载环境变量
load_dotenv()
# 讯飞API配置
XUNFEI_CONFIG = {
    'APP_ID': 'af632c9a',
    'API_KEY': os.getenv('XUNFEI_API_KEY'),
    'API_SECRET': os.getenv('XUNFEI_API_SECRET'),
    'FACE_API_URL': 'https://api.xf-yun.com/v1/private/s67c9c78c'
}
# 数据库配置
DATABASE_CONFIG = {
    'TYPE': os.getenv('DB_TYPE', 'mysql'),  # 改为'mysql'
    'HOST': os.getenv('DB_HOST', 'localhost'),
    'PORT': int(os.getenv('DB_PORT', 3306)),  # MySQL 默认端口3306
    'NAME': os.getenv('DB_NAME', 'vimi'),
    'USER': os.getenv('DB_USER', 'root'),  # MySQL常用root用户
    'PASSWORD': os.getenv('DB_PASSWORD', '123456')
}

# Flask应用配置
FLASK_CONFIG = {
    'SECRET_KEY': os.getenv('FLASK_SECRET_KEY', 'dev'),
    'DEBUG': os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
}