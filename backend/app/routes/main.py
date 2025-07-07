from flask import Blueprint, jsonify, request, send_from_directory, current_app
import os

bp = Blueprint('main', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@bp.route('/')
def index():
    """主页路由"""
    return jsonify({
        'status': 'ok',
        'message': 'Welcome to VIMI API'
    })

@bp.route('/health')
def health_check():
    """健康检查路由"""
    return jsonify({
        'status': 'ok',
        'message': 'Service is healthy'
    })

@bp.route('/api/test')
def test():
    """API测试路由"""
    return jsonify({
        'status': 'ok',
        'message': 'API test successful'
    })

@bp.route('/api/upload_audio', methods=['POST'])
def upload_audio():
    """音频文件上传接口，接收form-data中的file字段，保存到uploads目录，返回文件路径"""
    file = request.files.get('file')
    if not file or not file.filename:
        return jsonify({'success': False, 'error': '未检测到文件或文件名为空'}), 400
    # 只允许部分音频格式
    allowed_ext = {'wav', 'mp3', 'm4a', 'webm'}
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext not in allowed_ext:
        return jsonify({'success': False, 'error': '不支持的音频格式'}), 400
    filename = file.filename
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)
    rel_path = f'uploads/{filename}'
    return jsonify({'success': True, 'path': rel_path, 'filename': filename})

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    # uploads 目录在 backend/app/uploads
    uploads_dir = os.path.join(current_app.root_path, 'uploads')
    return send_from_directory(uploads_dir, filename)