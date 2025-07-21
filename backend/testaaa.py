from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        with db.engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            scalar = result.scalar()
        if scalar == 1:
            print("数据库连接成功")
        else:
            print("数据库连接异常")
    except Exception as e:
        print("数据库连接失败:", e)
