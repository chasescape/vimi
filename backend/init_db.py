import pymysql
import sys
from app import create_app, db

def init_database():
    try:
        # 连接MySQL
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='123456'
        )
        
        with connection.cursor() as cursor:
            # 创建数据库（如果不存在）
            cursor.execute("CREATE DATABASE IF NOT EXISTS dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("数据库'dev'创建成功或已存在")
            
        connection.close()
        
        # 初始化Flask应用
        app = create_app('development')
        
        with app.app_context():
            # 创建所有表
            db.create_all()
            print("所有数据库表创建成功")
            
        return True
        
    except Exception as e:
        print(f"初始化数据库时出错: {e}")
        return False

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1) 