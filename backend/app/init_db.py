from app import create_app, db
from app.models.user import User
from datetime import datetime

def init_db():
    app = create_app()
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 检查是否已存在测试用户
        if not User.query.filter_by(username='test').first():
            # 创建测试用户
            test_user = User(
                email='test@example.com',
                username='test',
                role='candidate',
                is_active=True,
                created_at=datetime.utcnow()
            )
            test_user.password = 'test123'  # 设置密码
            
            # 创建测试面试官
            test_interviewer = User(
                email='interviewer@example.com',
                username='interviewer',
                role='interviewer',
                is_active=True,
                created_at=datetime.utcnow(),
                invite_code='VIMI2024'
            )
            test_interviewer.password = 'test123'
            
            # 添加到数据库
            db.session.add(test_user)
            db.session.add(test_interviewer)
            db.session.commit()
            print("测试用户创建成功！")
            print("应聘者账号: test / test123")
            print("面试官账号: interviewer / test123")
        else:
            print("测试用户已存在！")

if __name__ == '__main__':
    init_db() 