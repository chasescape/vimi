from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """主页路由"""
    return jsonify({
        'status': 'ok',
        'message': 'Welcome to VIMI API'
    })

@bp.route('/health')
def health_check():
    """健康检查路由"""
    return jsonify({
        'status': 'ok',
        'message': 'Service is healthy'
    })

@bp.route('/api/test')
def test():
    """API测试路由"""
    return jsonify({
        'status': 'ok',
        'message': 'API test successful'
    }) 