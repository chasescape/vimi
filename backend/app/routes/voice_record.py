import re
import json
from flask import Blueprint, request, jsonify
from app.models.voice_record import VoiceRecord
from app import db
from datetime import datetime
from app.spark_ai import ask_spark_model

voice_record_bp = Blueprint('voice_record', __name__, url_prefix='/voice_record')

@voice_record_bp.route('/save', methods=['POST'])
def save_and_analyse():
    data = request.get_json(silent=True) or {}
    transcription = data.get('transcription')
    user_id = data.get('user_id', 1)

    if not transcription:
        return jsonify({'msg': 'transcription为必填项'}), 400

    # 先保存转写文本
    record = VoiceRecord(
        user_id=user_id,
        transcription=transcription,
        created_at=datetime.utcnow()
    )
    db.session.add(record)
    db.session.commit()

    try:
        # 调用星火大模型进行情绪分析
        raw_sentiment = ask_spark_model(transcription)

        # 清理返回内容，去除 ```json``` 包裹或多余内容
        clean_str = re.sub(r'```json|```', '', raw_sentiment).strip()

        # 转换成 JSON 对象
        sentiment_obj = json.loads(clean_str)

        # 存入数据库（存字符串）
        record.sentiment = json.dumps(sentiment_obj, ensure_ascii=False)
        db.session.commit()

        return jsonify({
            'msg': '保存并分析成功',
            'id': record.id,
            'sentiment': sentiment_obj
        }), 200

    except Exception as e:
        return jsonify({
            'msg': '情绪分析失败',
            'id': record.id,
            'error': str(e)
        }), 500
###获取最新情绪进行展示，避免刷新
@voice_record_bp.route('/latest_sentiment', methods=['GET'])
def get_latest_sentiment():
    user_id = 1  # 固定用户ID

    latest_record = (
        VoiceRecord.query
        .filter_by(user_id=user_id)
        .filter(VoiceRecord.sentiment != None)
        .order_by(VoiceRecord.created_at.desc())
        .first()
    )

    if not latest_record:
        return jsonify({'msg': '没有找到情绪分析数据', 'sentiment': {}}), 404

    try:
        sentiment_obj = json.loads(latest_record.sentiment)
    except Exception:
        sentiment_obj = {}

    return jsonify({
        'msg': '获取成功',
        'sentiment': sentiment_obj,
        'record_id': latest_record.id,
        'created_at': latest_record.created_at.isoformat()
    }), 200
