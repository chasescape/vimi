from app import create_app
from app import db
app = create_app()

if __name__ == '__main__':
    # 使用 0.0.0.0 允许外部访问，端口 5000
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)