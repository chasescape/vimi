from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app.models.user import SpeechRecord
from app import db
from .speech_recognition import SpeechRecognition

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
UPLOAD_FOLDER = 'uploads'
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
    """语音识别API"""
    try:
        print("=== 语音识别API被调用 ===")
        data = request.get_json()
        print(f"接收到的数据: {data}")
        
        audio_file_path = data.get('audio_file_path')
        user_id = data.get('user_id')
        is_realtime = data.get('is_realtime', False)
        
        print(f"音频文件路径: {audio_file_path}")
        print(f"用户ID: {user_id}")
        print(f"是否实时录音: {is_realtime}")
        
        if not audio_file_path:
            print("错误: 音频文件路径是必需的")
            return jsonify({'error': '音频文件路径是必需的'}), 400
        
        # 检查文件是否存在
        print(f"检查文件是否存在: {audio_file_path}")
        if not os.path.exists(audio_file_path):
            print(f"文件不存在，尝试在uploads目录中查找")
            # 尝试在uploads目录中查找
            uploads_path = os.path.join(UPLOAD_FOLDER, os.path.basename(audio_file_path))
            print(f"uploads路径: {uploads_path}")
            if os.path.exists(uploads_path):
                audio_file_path = uploads_path
                print(f"在uploads目录中找到文件: {audio_file_path}")
            else:
                print(f"文件在uploads目录中也不存在")
                return jsonify({'error': f'音频文件不存在: {audio_file_path}'}), 404
        
        print(f"开始语音识别: {audio_file_path}")
        
        # 执行语音识别
        result = speech_recognizer.recognize_audio_file(audio_file_path)
        
        print(f"识别结果: {result}")
        
        if result['success']:
            # 保存识别记录到数据库
            speech_record = SpeechRecord(
                audio_file=audio_file_path,
                recognized_text=result['text'],
                user_id=user_id
            )
            db.session.add(speech_record)
            db.session.commit()
            
            print("识别成功，记录已保存")
            return jsonify({
                'success': True,
                'text': result['text'],
                'record_id': speech_record.id,
                'is_realtime': is_realtime
            })
        else:
            # 增强错误提示
            error_msg = result['error'] or '识别结果为空，可能音频内容无效或格式不兼容。请上传16kHz/16bit/单声道wav音频。'
            print(f"识别失败: {error_msg}")
            return jsonify({
                'success': False,
                'error': error_msg,
                'is_realtime': is_realtime
            }), 400
            
    except Exception as e:
        print(f"语音识别异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'语音识别失败: {str(e)}'}), 500

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
