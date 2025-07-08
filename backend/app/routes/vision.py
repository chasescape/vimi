from flask import Blueprint, request, jsonify
import base64
import re
from ..services.ai.vision.face_recognition import FaceRecognitionService
import requests
from app.services.ai.vision.face_verify import FaceVerifyService
from app.services.ai.vision.face_detect import FaceDetectService

vision_bp = Blueprint('vision', __name__)
face_service = FaceRecognitionService()
face_verify_service = FaceVerifyService()
face_detect_service = FaceDetectService()

def extract_base64_data(data_url):
    """从Data URL中提取Base64数据"""
    pattern = r'^data:image/[a-zA-Z]+;base64,(.+)$'
    match = re.match(pattern, data_url)
    if match:
        return match.group(1)
    return data_url  # 如果不是Data URL格式，假设是纯Base64数据

@vision_bp.route('/face/verify', methods=['POST'])
async def verify_face():
    """
    人脸验证接口
    
    请求体格式：
    {
        "id_photo": "base64编码的证件照",
        "live_photo": "base64编码的实时照片"
    }
    
    返回格式：
    {
        "success": true/false,
        "is_same_person": true/false,
        "confidence": float,
        "error": "错误信息"
    }
    """
    try:
        data = request.get_json()
        
        # 验证请求数据
        if not data or 'id_photo' not in data or 'live_photo' not in data:
            return jsonify({
                'success': False,
                'error': '请求数据不完整'
            }), 400
            
        # 提取并解码Base64图片数据
        try:
            id_photo_base64 = extract_base64_data(data['id_photo'])
            live_photo_base64 = extract_base64_data(data['live_photo'])
            
            id_photo_data = base64.b64decode(id_photo_base64)
            live_photo_data = base64.b64decode(live_photo_base64)
            
            # 验证图片数据是否为空
            if not id_photo_data or not live_photo_data:
                return jsonify({
                    'success': False,
                    'error': '图片数据为空'
                }), 400
                
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'图片数据格式错误: {str(e)}'
            }), 400
            
        # 调用人脸验证服务
        is_same_person, confidence, error = await face_service.verify_face(
            id_photo_data,
            live_photo_data
        )
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 500
            
        return jsonify({
            'success': True,
            'is_same_person': is_same_person,
            'confidence': confidence
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500

@vision_bp.route('/proxy/xf-yun', methods=['POST'])
def proxy_xf_yun():
    try:
        # 从请求中获取所有需要的信息
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            # 添加讯飞API所需的认证信息
            'Authorization': request.headers.get('Authorization')
        }
        
        # 转发请求到讯飞API
        response = requests.post(
            'https://api.xf-yun.com' + request.path,
            headers=headers,
            json=request.json,
            verify=True  # 验证SSL证书
        )
        
        return jsonify(response.json()), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': '代理请求失败',
            'message': str(e)
        }), 500

@vision_bp.route('/face/detect', methods=['POST'])
def detect_face():
    """
    人脸检测和属性分析接口
    
    请求体格式：
    {
        "image_base64": "base64编码的图片数据或Data URL"
    }
    
    返回格式：
    {
        "success": true/false,
        "face_count": int,
        "faces": [
            {
                "score": float,
                "location": {
                    "x": int,
                    "y": int,
                    "width": int,
                    "height": int
                },
                "properties": {
                    "expression": string,
                    "gender": string,
                    "glass": string,
                    "hair": string,
                    "beard": string,
                    "mask": string
                }
            }
        ],
        "error": "错误信息"
    }
    """
    try:
        data = request.get_json()
        
        # 验证请求数据
        if not data or 'image_base64' not in data:
            return jsonify({
                'success': False,
                'error': '请提供图片数据 (image_base64)'
            }), 400

        # 提取并验证base64数据
        try:
            image_base64 = extract_base64_data(data['image_base64'])
            image_data = base64.b64decode(image_base64)
            
            # 验证图片数据是否为空
            if not image_data:
                return jsonify({
                    'success': False,
                    'error': '图片数据为空'
                }), 400
                
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'图片数据格式错误: {str(e)}'
            }), 400

        # 调用人脸检测服务
        result = face_detect_service.analyze_face(image_base64)
        
        if not result['success']:
            return jsonify(result), 500
            
        return jsonify(result)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500 