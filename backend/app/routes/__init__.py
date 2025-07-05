from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return {'message': '后端服务已启动'}, 200

@main_bp.route('/health')
def health():
    return {'status': 'ok'}, 200 