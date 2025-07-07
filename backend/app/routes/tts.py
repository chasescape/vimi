from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app.models.user import SpeechRecord
from app import db
from ..services.ai.tts.text_to_speech import TextToSpeech
from flask import Blueprint, request, jsonify
from flask_socketio import Namespace, emit
from ..services.ai.tts.text_to_speech import TextToSpeech
from app import socketio
import base64
import tempfile
import os
tts_bp = Blueprint('tts', __name__)

# 科大讯飞语音合成配置
SPEECH_CONFIG = {
    'APPID': 'ea0e453f',
    'APIKey': 'cfe0b8933be42c3dfcf6e1d3e2f2882e',
    'APISecret': 'ZWI5NGJhOGJmZGQ5ZDM5MTU0ZWExMGVk'
}

# 初始化语音合成
text_to_speech = TextToSpeech(
    app_id=SPEECH_CONFIG['APPID'],
    api_key=SPEECH_CONFIG['APIKey'],
    api_secret=SPEECH_CONFIG['APISecret']
)

# 文件上传配置
UPLOAD_FOLDER = 'app/uploads'
ALLOWED_EXTENSIONS = {'txt', 'md', 'doc', 'docx'}

# 创建上传目录
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@tts_bp.route('/upload', methods=['POST'])
def upload_text():
    """上传文本文件"""
    try:
        if 'text_file' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400
        
        file = request.files['text_file']
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

@tts_bp.route('/synthesize', methods=['POST'])
def synthesize_speech():
    """文字转语音API"""
    try:
        print("=== 文字转语音API被调用 ===")
        data = request.get_json()
        print(f"接收到的数据: {data}")
        
        text = data.get('text')
        user_id = data.get('user_id')
        output_filename = data.get('output_filename')
        
        print(f"文本内容: {text[:50]}..." if text else "无文本")
        print(f"用户ID: {user_id}")
        print(f"输出文件名: {output_filename}")
        
        if not text or not text.strip():
            print("错误: 文本内容是必需的")
            return jsonify({'error': '文本内容是必需的'}), 400
        
        # 生成输出文件路径
        if output_filename:
            output_file_path = os.path.join(UPLOAD_FOLDER, output_filename)
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file_path = os.path.join(UPLOAD_FOLDER, f"synthesized_{timestamp}.mp3")
        
        print(f"开始文字转语音: {text[:50]}...")
        print(f"输出文件: {output_file_path}")
        
        # 执行文字转语音
        result = text_to_speech.synthesize_text(text, output_file_path)
        
        print(f"合成结果: {result}")
        
        if result['success']:
            # 获取音频文件大小
            file_size = os.path.getsize(output_file_path) if os.path.exists(output_file_path) else 0
            
            # 保存合成记录到数据库
            speech_record = SpeechRecord(
                audio_file=output_file_path,
                recognized_text=text,  # 对于TTS，这里存储原始文本
                user_id=user_id
            )
            db.session.add(speech_record)
            db.session.commit()
            
            print("合成成功，记录已保存")
            return jsonify({
                'success': True,
                'audio_file_path': output_file_path,
                'audio_url': f'/uploads/{os.path.basename(output_file_path)}',
                'file_size': file_size,
                'record_id': speech_record.id,
                'duration': 0.0  # TODO: 计算音频时长
            })
        else:
            # 增强错误提示
            error_msg = result['error'] or '合成失败，请检查文本内容或网络连接。'
            print(f"合成失败: {error_msg}")
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400
            
    except Exception as e:
        print(f"文字转语音异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'文字转语音失败: {str(e)}'}), 500

@tts_bp.route('/synthesize_file', methods=['POST'])
def synthesize_from_file():
    """从文件合成语音"""
    try:
        print("=== 从文件合成语音API被调用 ===")
        data = request.get_json()
        print(f"接收到的数据: {data}")
        
        text_file_path = data.get('text_file_path')
        user_id = data.get('user_id')
        output_filename = data.get('output_filename')
        
        print(f"文本文件路径: {text_file_path}")
        print(f"用户ID: {user_id}")
        print(f"输出文件名: {output_filename}")
        
        if not text_file_path:
            print("错误: 文本文件路径是必需的")
            return jsonify({'error': '文本文件路径是必需的'}), 400
        
        # 检查文件是否存在
        print(f"检查文件是否存在: {text_file_path}")
        if not os.path.exists(text_file_path):
            print(f"文件不存在，尝试在uploads目录中查找")
            # 尝试在uploads目录中查找
            uploads_path = os.path.join(UPLOAD_FOLDER, os.path.basename(text_file_path))
            print(f"uploads路径: {uploads_path}")
            if os.path.exists(uploads_path):
                text_file_path = uploads_path
                print(f"在uploads目录中找到文件: {text_file_path}")
            else:
                print(f"文件在uploads目录中也不存在")
                return jsonify({'error': f'文本文件不存在: {text_file_path}'}), 404
        
        # 读取文本文件
        try:
            with open(text_file_path, 'r', encoding='utf-8') as f:
                text = f.read().strip()
        except Exception as e:
            print(f"读取文件失败: {str(e)}")
            return jsonify({'error': f'读取文本文件失败: {str(e)}'}), 500
        
        if not text:
            print("错误: 文本文件为空")
            return jsonify({'error': '文本文件为空'}), 400
        
        print(f"读取到的文本: {text[:50]}...")
        
        # 生成输出文件路径
        if output_filename:
            output_file_path = os.path.join(UPLOAD_FOLDER, output_filename)
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file_path = os.path.join(UPLOAD_FOLDER, f"synthesized_{timestamp}.mp3")
        
        print(f"开始从文件合成语音")
        print(f"输出文件: {output_file_path}")
        
        # 执行文字转语音
        result = text_to_speech.synthesize_text(text, output_file_path)
        
        print(f"合成结果: {result}")
        
        if result['success']:
            # 获取音频文件大小
            file_size = os.path.getsize(output_file_path) if os.path.exists(output_file_path) else 0
            
            # 保存合成记录到数据库
            speech_record = SpeechRecord(
                audio_file=output_file_path,
                recognized_text=text,  # 对于TTS，这里存储原始文本
                user_id=user_id
            )
            db.session.add(speech_record)
            db.session.commit()
            
            print("合成成功，记录已保存")
            return jsonify({
                'success': True,
                'audio_file_path': output_file_path,
                'audio_url': f'/uploads/{os.path.basename(output_file_path)}',
                'file_size': file_size,
                'record_id': speech_record.id,
                'duration': 0.0  # TODO: 计算音频时长
            })
        else:
            # 增强错误提示
            error_msg = result['error'] or '合成失败，请检查文本内容或网络连接。'
            print(f"合成失败: {error_msg}")
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400
            
    except Exception as e:
        print(f"从文件合成语音异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'从文件合成语音失败: {str(e)}'}), 500

@tts_bp.route('/records', methods=['GET'])
def get_synthesis_records():
    """获取语音合成记录"""
    records = SpeechRecord.query.order_by(SpeechRecord.created_at.desc()).all()
    return jsonify([{
        'id': record.id,
        'audio_file': record.audio_file,
        'recognized_text': record.recognized_text,
        'user_id': record.user_id,
        'created_at': record.created_at.isoformat()
    } for record in records])

@tts_bp.route('/records/<int:record_id>', methods=['GET'])
def get_synthesis_record(record_id):
    """获取单个语音合成记录"""
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

class TTSStreamNamespace(Namespace):
    def on_connect(self):
        print('客户端已连接')
        self.text_buffer = ''

    def on_disconnect(self):
        print('客户端已断开')
        self.text_buffer = ''

    def on_text_stream(self, data):
        # data: {"text": "本次的一段文本", "is_last": false}
        text = data.get('text', '')
        is_last = data.get('is_last', False)
        print('收到文本片段:', text)
        self.text_buffer += text
        if is_last:
            # 合成全部文本
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmpfile:
                output_path = tmpfile.name
            result = text_to_speech.synthesize_text(self.text_buffer, output_path)
            if result['success']:
                with open(output_path, 'rb') as f:
                    audio_bytes = f.read()
                audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
                emit('tts_audio', {'audio': audio_base64, 'is_last': True})
                os.remove(output_path)
            else:
                emit('tts_error', {'error': result['error']})
            self.text_buffer = ''
        else:
            # 可以选择返回进度或不返回
            emit('tts_progress', {'received': len(self.text_buffer)})

# 注册命名空间

def register_tts_stream_namespace():
    socketio.on_namespace(TTSStreamNamespace('/api/tts/stream')) 