from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app.models.speech import SpeechRecord
from app import db
from ..services.ai.asr.speech_recognition import SpeechRecognition

asr_bp = Blueprint('asr', __name__)

# 科大讯飞语音识别配置
SPEECH_CONFIG = {
    'APPID': 'fd2e4312',
    'APIKey': '0c704fe4c2b9696f3194ffff37152b56',
    'APISecret': 'MzY1ZmQ2OTY2NGVhMzhjM2NmZjAzNDli'
}

# 初始化语音识别
speech_recognizer = SpeechRecognition(
    app_id=SPEECH_CONFIG['APPID'],
    api_key=SPEECH_CONFIG['APIKey'],
    api_secret=SPEECH_CONFIG['APISecret']
)

# 文件上传配置
UPLOAD_FOLDER = 'app/uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'aac', 'flac', 'webm'}

# 创建上传目录
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@asr_bp.route('/upload', methods=['POST'])
def upload_audio():
    """上传音频文件"""
    try:
        if 'audio_file' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400
        
        file = request.files['audio_file']
        if file.filename == '' or file.filename is None:
            return jsonify({'error': '没有选择文件'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename or '')
            # 添加时间戳避免文件名冲突
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'filepath': filepath
            })
        else:
            return jsonify({'error': '不支持的文件格式'}), 400
            
    except Exception as e:
        return jsonify({'error': f'文件上传失败: {str(e)}'}), 500

@asr_bp.route('/recognize', methods=['POST'])
def recognize_speech():
    """语音识别接口"""
    try:
        # 检查是否有文件上传
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'message': '没有上传音频文件'
            }), 400
            
        audio_file = request.files['audio']
        user_id = request.form.get('user_id')
        
        # 检查文件名
        if audio_file.filename == '':
            return jsonify({
                'success': False,
                'message': '没有选择文件'
            }), 400
        
        # 保存音频文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"audio_{timestamp}.wav"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        audio_file.save(filepath)
        
        # 初始化语音识别服务
        asr_service = SpeechRecognition()
        
        # 执行语音识别
        result = asr_service.recognize(filepath)
        
        if result['success']:
            # 保存记录到数据库
            record = SpeechRecord(
                audio_file=filepath,
                recognized_text=result['text'],
                user_id=user_id
            )
            db.session.add(record)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'text': result['text'],
                'record_id': record.id
            })
        else:
            return jsonify({
                'success': False,
                'message': result['error']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'语音识别失败: {str(e)}'
        }), 500

@asr_bp.route('/records', methods=['GET'])
def get_speech_records():
    """获取语音识别记录"""
    records = SpeechRecord.query.order_by(SpeechRecord.created_at.desc()).all()
    return jsonify([{
        'id': record.id,
        'audio_file': record.audio_file,
        'recognized_text': record.recognized_text,
        'user_id': record.user_id,
        'created_at': record.created_at.isoformat()
    } for record in records])

@asr_bp.route('/records/<int:record_id>', methods=['GET'])
def get_speech_record(record_id):
    """获取单个语音识别记录"""
    record = SpeechRecord.query.get(record_id)
    if not record:
        return jsonify({'error': '记录不存在'}), 404
    
    return jsonify({
        'id': record.id,
        'audio_file': record.audio_file,
        'recognized_text': record.recognized_text,
        'user_id': record.user_id,
        'created_at': record.created_at.isoformat()
    })
