from flask import Blueprint, request, jsonify
import os
import traceback
from app.services.ai.llm import X1_http

spark_bp = Blueprint('spark', __name__)

@spark_bp.route('/chat', methods=['POST'])
def spark_chat():
    """星火大模型对话接口"""
    try:
        data = request.get_json()
        if not data or 'messages' not in data:
            return jsonify({'error': '缺少messages参数'}), 400
        messages = data['messages']
        if not isinstance(messages, list) or len(messages) == 0:
            return jsonify({'error': 'messages参数应为非空列表'}), 400

        # 调用星火大模型
        reply = X1_http.get_answer(messages)
        return jsonify({'success': True, 'reply': reply})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'星火大模型对话失败: {str(e)}'}), 500 