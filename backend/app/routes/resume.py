from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import json
import uuid

from ..models.resume import Resume
from ..utils.auth import candidate_required
from .. import db

resume_bp = Blueprint('resume', __name__)

@resume_bp.route('/', methods=['GET'])
@candidate_required
def get_resumes():
    """获取当前用户的所有简历"""
    user_id = get_jwt_identity()
    resumes = Resume.query.filter_by(user_id=user_id).all()
    return jsonify({
        'success': True,
        'data': [resume.to_dict() for resume in resumes]
    })

@resume_bp.route('/', methods=['POST'])
@candidate_required
def create_resume():
    """创建新简历"""
    user_id = get_jwt_identity()
    data = request.json
    
    try:
        resume = Resume(
            user_id=user_id,
            name=data.get('name', '未命名简历'),
            content=data.get('content', {}),
        )
        db.session.add(resume)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '创建成功',
            'data': resume.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@resume_bp.route('/<int:resume_id>', methods=['PUT'])
@candidate_required
def update_resume(resume_id):
    """更新简历"""
    user_id = get_jwt_identity()
    resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
    
    if not resume:
        return jsonify({
            'success': False,
            'message': '简历不存在或无权访问'
        }), 404
    
    data = request.json
    try:
        if 'name' in data:
            resume.name = data['name']
        if 'content' in data:
            resume.content = data['content']
        resume.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '更新成功',
            'data': resume.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@resume_bp.route('/<int:resume_id>', methods=['DELETE'])
@candidate_required
def delete_resume(resume_id):
    """删除简历"""
    user_id = get_jwt_identity()
    resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
    
    if not resume:
        return jsonify({
            'success': False,
            'message': '简历不存在或无权访问'
        }), 404
    
    try:
        db.session.delete(resume)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '删除成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@resume_bp.route('/<int:resume_id>/duplicate', methods=['POST'])
@candidate_required
def duplicate_resume(resume_id):
    """复制简历"""
    user_id = get_jwt_identity()
    resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
    
    if not resume:
        return jsonify({
            'success': False,
            'message': '简历不存在或无权访问'
        }), 404
    
    try:
        new_resume = Resume(
            user_id=user_id,
            name=f"{resume.name} (副本)",
            content=resume.content.copy() if resume.content else {},
        )
        db.session.add(new_resume)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '复制成功',
            'data': new_resume.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@resume_bp.route('/<int:resume_id>/share', methods=['POST'])
@candidate_required
def share_resume(resume_id):
    """生成简历分享链接"""
    user_id = get_jwt_identity()
    resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
    
    if not resume:
        return jsonify({
            'success': False,
            'message': '简历不存在或无权访问'
        }), 404
    
    try:
        share_code = str(uuid.uuid4())[:8]
        resume.share_code = share_code
        resume.share_expire_time = datetime.utcnow().timestamp() + 7 * 24 * 3600  # 7天后过期
        db.session.commit()
        
        share_url = f"{request.host_url}resume/share/{share_code}"
        return jsonify({
            'success': True,
            'message': '分享链接生成成功',
            'data': {
                'share_code': share_code,
                'share_url': share_url,
                'expire_time': resume.share_expire_time
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@resume_bp.route('/share/<share_code>', methods=['GET'])
def view_shared_resume(share_code):
    """查看分享的简历"""
    resume = Resume.query.filter_by(share_code=share_code).first()
    
    if not resume or not resume.is_share_valid():
        return jsonify({
            'success': False,
            'message': '分享链接无效或已过期'
        }), 404
    
    return jsonify({
        'success': True,
        'data': resume.to_dict()
    }) 