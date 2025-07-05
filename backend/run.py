from app import create_app

app = create_app()
 
if __name__ == '__main__':
    # 使用 0.0.0.0 允许外部访问，端口 5000
    app.run()