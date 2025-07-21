from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash
from app.models.user import User
from app import db
import jwt
import datetime
import logging

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册接口"""
    try:
        data = request.get_json()
        current_app.logger.info(f"收到注册请求数据: {data}")
        
        # 验证必要字段
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                current_app.logger.warning(f"缺少必要字段: {field}")
                return jsonify({
                    'success': False,
                    'message': f'缺少必要字段: {field}'
                }), 400

        # 检查用户名是否已存在
        if User.query.filter_by(username=data['username']).first():
            current_app.logger.warning(f"用户名已存在: {data['username']}")
            return jsonify({
                'success': False,
                'message': '用户名已存在'
            }), 400

        # 检查邮箱是否已存在
        if User.query.filter_by(email=data['email']).first():
            current_app.logger.warning(f"邮箱已被注册: {data['email']}")
            return jsonify({
                'success': False,
                'message': '邮箱已被注册'
            }), 400

        # 创建新用户
        try:
            new_user = User(
                username=data['username'],
                email=data['email'],
                role=1 if data.get('role') == 'interviewer' else 2  # 1为面试官，2为应聘者
            )
            new_user.set_password(data['password'])
            current_app.logger.info(f"创建新用户: {new_user.username}")

            # 保存到数据库
            db.session.add(new_user)
            db.session.commit()
            current_app.logger.info(f"用户保存成功: {new_user.id}")

            return jsonify({
                'success': True,
                'message': '注册成功',
                'data': {
                    'user_id': new_user.id,
                    'username': new_user.username,
                    'email': new_user.email,
                    'role': new_user.role
                }
            }), 201

        except Exception as e:
            current_app.logger.error(f"创建用户时出错: {str(e)}")
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'创建用户失败: {str(e)}'
            }), 500

    except Exception as e:
        current_app.logger.error(f"注册过程中出错: {str(e)}")
        if 'data' in locals():
            current_app.logger.error(f"请求数据: {data}")
        return jsonify({
            'success': False,
            'message': f'注册失败: {str(e)}'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录接口"""
    try:
        data = request.get_json()
        
        # 验证必要字段
        if not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': '请提供用户名和密码'
            }), 400
        
        # 查找用户
        user = User.query.filter_by(username=data['username']).first()
        
        # 验证用户存在性和密码
        if not user or not user.check_password(data['password']):
            return jsonify({
                'success': False,
                'message': '用户名或密码错误'
            }), 401
        
        # 生成JWT token
        token = jwt.encode(
            {
                'user_id': user.id,
                'username': user.username,
                'role': user.role,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        
        # 更新最后登录时间
        user.last_login = datetime.datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '登录成功',
            'data': {
                'access_token': token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'登录失败: {str(e)}'
        }), 500

@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """验证token有效性"""
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({
                'success': False,
                'message': '未提供token'
            }), 401

        # 去除Bearer前缀
        if token.startswith('Bearer '):
            token = token[7:]

        # 验证token
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user = User.query.get(payload['user_id'])
            
            if not user:
                raise jwt.InvalidTokenError('用户不存在')

            return jsonify({
                'success': True,
                'message': 'token有效',
                'data': {
                    'user_id': user.id,
                    'username': user.username,
                    'role': user.role
                }
            }), 200
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'message': 'token已过期'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'message': '无效的token'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'验证失败: {str(e)}'
        }), 500
