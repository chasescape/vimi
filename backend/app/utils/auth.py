from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from ..models.user import User

def role_required(roles):
    """
    检查用户角色的装饰器
    :param roles: 允许的角色列表，如 ['candidate', 'interviewer']
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({
                    'success': False,
                    'message': '用户不存在'
                }), 401
                
            if user.role not in roles:
                return jsonify({
                    'success': False,
                    'message': '无权访问'
                }), 403
                
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def candidate_required(fn):
    """应聘者权限装饰器"""
    return role_required(['candidate'])(fn)

def interviewer_required(fn):
    """面试官权限装饰器"""
    return role_required(['interviewer'])(fn)

def admin_required(fn):
    """管理员权限装饰器"""
    return role_required(['admin'])(fn) 