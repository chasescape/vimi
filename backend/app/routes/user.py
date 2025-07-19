from flask import Blueprint, request, jsonify
import base64
import os
from PIL import Image
from io import BytesIO
from ..services.ai.vision.face_recognition import FaceRecognitionService
from app.models.user import User
user_bp = Blueprint('user', __name__)
face_service = FaceRecognitionService()
from app.models.job import Job
from app.models.jobApplication import JobApplication
# 存储用户照片的目录
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@user_bp.route('/upload-id-photo', methods=['POST'])
def upload_id_photo():
    """上传证件照接口"""
    try:
        data = request.get_json()
        if not data or 'photo' not in data:
            return jsonify({
                'success': False,
                'error': '请求数据不完整'
            }), 400

        # 解码Base64图片数据
        try:
            # 去除Base64前缀
            if ',' in data['photo']:
                photo_data = data['photo'].split(',')[1]
            else:
                photo_data = data['photo']
            
            # 解码Base64数据
            image_data = base64.b64decode(photo_data)
            
            # 验证图片格式
            image = Image.open(BytesIO(image_data))
            
            # 生成文件名
            filename = 'id_photo.jpg'
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            # 保存图片
            with open(filepath, 'wb') as f:
                f.write(image_data)
                
            return jsonify({
                'success': True,
                'message': '证件照上传成功',
                'filename': filename
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'图片处理失败: {str(e)}'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500

@user_bp.route('/verify-face', methods=['POST'])
def verify_face():
    """上传实时照片并进行人脸验证"""
    try:
        data = request.get_json()
        if not data or 'live_photo' not in data:
            return jsonify({
                'success': False,
                'error': '请求数据不完整'
            }), 400

        # 获取证件照路径
        id_photo_path = os.path.join(UPLOAD_FOLDER, 'id_photo.jpg')
        if not os.path.exists(id_photo_path):
            return jsonify({
                'success': False,
                'error': '请先上传证件照'
            }), 400

        try:
            # 读取证件照
            with open(id_photo_path, 'rb') as f:
                id_photo_data = f.read()

            # 处理实时照片 base64
            if ',' in data['live_photo']:
                live_photo_base64 = data['live_photo'].split(',')[1]
            else:
                live_photo_base64 = data['live_photo']
            
            # 解码实时照片
            live_photo_data = base64.b64decode(live_photo_base64)

            # 调用人脸验证服务
            is_same_person, score, error = face_service.verify_face(id_photo_data, live_photo_data)

            if error:
                return jsonify({
                    'success': False,
                    'error': error
                }), 500

            return jsonify({
                'success': True,
                'is_same_person': is_same_person,
                'confidence': score
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'图片处理失败: {str(e)}'
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500

###获取应聘者信息
@user_bp.route('/job_info', methods=['GET'])
def get_user_job_info():
    user_id = request.args.get('user_id', type=int)
    job_id = request.args.get('job_id', type=int)

    if not user_id or not job_id:
        return jsonify({'msg': '缺少 user_id 或 job_id 参数'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': '未找到指定用户'}), 404

    job = Job.query.get(job_id)
    if not job:
        return jsonify({'msg': '未找到指定职位'}), 404

    # 这里应该查询该用户对该职位的申请记录，而不是只按user_id查询
    job_application = JobApplication.query.filter_by(
        user_id=user_id,
        job_id=job_id
    ).first()

    if not job_application:
        return jsonify({'msg': '该用户没有申请该职位'}), 404

    return jsonify({
        'username': user.username,
        'job_title': job.job_title,
        'job_category': job.job_category,
        'photo_path': job_application.photo_path

    })
