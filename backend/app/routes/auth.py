from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import logging
import random
import string

from ..models.user import User
from .. import db

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

def generate_verification_code():
    """生成6位数字验证码"""
    return ''.join(random.choices(string.digits, k=6))

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        captcha = data.get('captcha')  # 前端验证码，可选

        if not username or not password:
            return jsonify({
                'success': False,
                'message': '用户名和密码不能为空'
            }), 400

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({
                'success': False,
                'message': '用户名或密码错误'
            }), 401

        if not user.verify_password(password):
            return jsonify({
                'success': False,
                'message': '用户名或密码错误'
            }), 401

        # 生成访问令牌
        access_token = create_access_token(
            identity=str(user.id),  # 强制转成字符串
            expires_delta=timedelta(days=1)
        )

        return jsonify({
            'success': True,
            'access_token': access_token,
            'user': user.to_dict()
        })

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({
            'success': False,
            'message': '登录失败，请稍后重试'
        }), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = data.get('role', 'candidate')  # 默认为求职者角色
        invite_code = data.get('inviteCode')  # 面试官邀请码，可选
        
        if not all([username, password, email]):
            return jsonify({
                'success': False,
                'message': '用户名、密码和邮箱不能为空'
            }), 400
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return jsonify({
                'success': False,
                'message': '用户名已存在'
            }), 400

        # 检查邮箱是否已存在
        if User.query.filter_by(email=email).first():
            return jsonify({
                'success': False,
                'message': '邮箱已被注册'
            }), 400

        # 如果是面试官，检查邀请码
        if role == 'interviewer':
            if not invite_code or invite_code != 'VIMI2024':  # 这里应该使用配置或数据库中的邀请码
                return jsonify({
                    'success': False,
                    'message': '邀请码无效'
            }), 400

        # 创建新用户
        user = User(
            username=username,
            password=password,  # 这里会调用setter方法进行加密
            role=role,
            email=email
        )
        db.session.add(user)
        db.session.commit()

        # 生成访问令牌
        access_token = create_access_token(
            identity=str(user.id),  # 强制转成字符串
            expires_delta=timedelta(days=1)
        )

        return jsonify({
            'success': True,
            'message': '注册成功',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Register error: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': '注册失败，请稍后重试'
        }), 500
###查看用户信息
@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()  # 拿到的是字符串
        user = User.query.get(int(user_id))  # 转成 int 查数据库

        if not user:
            return jsonify({'success': False, 'message': '用户不存在'}), 404

        return jsonify({'success': True, 'user': user.to_dict()}), 200
    except Exception as e:
        logger.error(f"Get profile error: {str(e)}")
        return jsonify({'success': False, 'message': '获取用户信息失败'}), 500



@auth_bp.route('/update', methods=['POST'])
@jwt_required()
def update_profile():
    """更新用户个人信息"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user:
            return jsonify({'success': False, 'message': '用户不存在'}), 404

        data = request.get_json()

        # 支持更新的字段
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        if 'phone' in data:
            user.phone = data['phone']
        if 'location' in data and isinstance(data['location'], dict):
            # 确保 location 不是 None
            user.location = data['location']

        db.session.commit()

        return jsonify({'success': True, 'message': '更新成功', 'user': user.to_dict()})
    except Exception as e:
        db.session.rollback()
        logger.error(f"Update profile error: {str(e)}")
        return jsonify({'success': False, 'message': '更新失败，请稍后重试'}), 500


@auth_bp.route('/send-code', methods=['POST'])
def send_verification_code():
    """发送验证码"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({
                'success': False,
                'message': '邮箱不能为空'
            }), 400

        # 生成验证码
        code = generate_verification_code()
        
        # TODO: 实际发送邮件的逻辑
        # 这里应该调用邮件服务发送验证码
        # 暂时直接返回验证码（仅用于开发测试）
        
        return jsonify({
            'success': True,
            'message': '验证码已发送',
            'code': code  # 实际生产环境不应该返回验证码
        })
        
    except Exception as e:
        logger.error(f"Send code error: {str(e)}")
        return jsonify({
            'success': False,
            'message': '发送验证码失败，请稍后重试'
        }), 500

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """重置密码"""
    try:
        data = request.get_json()
        email = data.get('email')
        code = data.get('code')
        new_password = data.get('newPassword')
        
        if not all([email, code, new_password]):
            return jsonify({
                'success': False,
                'message': '邮箱、验证码和新密码不能为空'
            }), 400

        # TODO: 验证验证码是否正确
        # 这里应该检查验证码是否匹配且在有效期内
        
        # 查找用户
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({
                'success': False,
                'message': '用户不存在'
            }), 404

        # 更新密码
        user.password = new_password
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '密码重置成功'
        })
        
    except Exception as e:
        logger.error(f"Reset password error: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': '重置密码失败，请稍后重试'
        }), 500
