from flask import Blueprint, request, jsonify
from datetime import datetime
from ..services.interview.interview_service import interview_service
from ..utils.validators import validate_date_format

# 创建蓝图
interview_bp = Blueprint('interview', __name__)

@interview_bp.route('/upcoming', methods=['GET'])
def get_upcoming_interview():
    """获取即将开始的面试"""
    user_id = request.args.get('user_id')  # 实际应该从认证中获取
    if not user_id:
        return jsonify({'error': '未提供用户ID'}), 400
        
    interview = interview_service.get_upcoming_interview(user_id)
    return jsonify(interview if interview else {})

@interview_bp.route('/statistics', methods=['GET'])
def get_interview_statistics():
    """获取面试统计信息"""
    user_id = request.args.get('user_id')  # 实际应该从认证中获取
    if not user_id:
        return jsonify({'error': '未提供用户ID'}), 400
        
    stats = interview_service.get_interview_statistics(user_id)
    return jsonify(stats)

@interview_bp.route('/history', methods=['GET'])
def get_interview_history():
    """获取面试历史记录"""
    user_id = request.args.get('user_id')  # 实际应该从认证中获取
    if not user_id:
        return jsonify({'error': '未提供用户ID'}), 400
        
    # 获取查询参数
    status = request.args.get('status')
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    
    # 转换日期格式
    start_date = None
    end_date = None
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': '开始日期格式无效'}), 400
            
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': '结束日期格式无效'}), 400
    
    history = interview_service.get_interview_history(
        user_id=user_id,
        status=status,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size
    )
    return jsonify(history)

@interview_bp.route('/start', methods=['POST'])
def start_interview():
    """开始新的面试"""
    data = request.get_json()
    user_id = data.get('user_id')  # 实际应该从认证中获取
    position = data.get('position')
    company = data.get('company')
    
    if not all([user_id, position, company]):
        return jsonify({'error': '缺少必要参数'}), 400
        
    try:
        interview_id = interview_service.start_interview(user_id, position, company)
        return jsonify({'interview_id': interview_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@interview_bp.route('/<interview_id>/questions', methods=['GET'])
def get_interview_questions(interview_id):
    """获取面试问题列表"""
    try:
        questions = interview_service.get_questions(interview_id)
        return jsonify({'questions': questions})
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@interview_bp.route('/<interview_id>/answer', methods=['POST'])
def submit_answer():
    """提交面试答案"""
    data = request.get_json()
    interview_id = data.get('interview_id')
    question_id = data.get('question_id')
    answer = data.get('answer')
    
    if not all([interview_id, question_id, answer]):
        return jsonify({'error': '缺少必要参数'}), 400
        
    try:
        evaluation = interview_service.add_answer(interview_id, question_id, answer)
        return jsonify(evaluation)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@interview_bp.route('/<interview_id>/end', methods=['POST'])
def end_interview(interview_id):
    """结束面试"""
    try:
        interview_service.end_interview(interview_id)
        return jsonify({'message': '面试已结束'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@interview_bp.route('/<interview_id>/evaluation', methods=['POST'])
def add_evaluation():
    """添加面试评估"""
    data = request.get_json()
    interview_id = data.get('interview_id')
    aspect = data.get('aspect')
    score = data.get('score')
    technical_score = data.get('technical_score')
    communication_score = data.get('communication_score')
    strengths = data.get('strengths', [])
    weaknesses = data.get('weaknesses', [])
    comment = data.get('comment')
    
    if not all([
        interview_id, aspect, score is not None,
        technical_score is not None, communication_score is not None,
        comment
    ]):
        return jsonify({'error': '缺少必要参数'}), 400
        
    try:
        interview_service.add_evaluation(
            interview_id=interview_id,
            aspect=aspect,
            score=score,
            technical_score=technical_score,
            communication_score=communication_score,
            strengths=strengths,
            weaknesses=weaknesses,
            comment=comment
        )
        return jsonify({'message': '评估已添加'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 