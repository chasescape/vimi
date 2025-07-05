import base64
import hashlib
import hmac
import json
import time
import requests
from datetime import datetime
from flask import current_app
from urllib.parse import urlparse
import asyncio

class FaceVerifyService:
    """科大讯飞人脸比对服务
    
    用于验证面试者身份
    """
    
    def __init__(self):
        """初始化服务，直接写死API凭证"""
        self.app_id = "af632c9a"
        self.api_key = "0f38b7916bc3ee000443a308b1d0d8da"
        self.api_secret = "ZGY3MGMyZjM1NjhjNjU3MzU3ZWQ0MDMw"
        self.api_url = "https://api.xf-yun.com/v1/private/s67c9c78c"

    def _create_signature(self, host, date, signature_origin):
        """生成请求签名"""
        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        return authorization

    def _prepare_headers(self, data):
        """准备HTTP请求头"""
        url = urlparse(self.api_url)
        host = url.netloc
        date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        signature_origin = f'host: {host}\ndate: {date}\nPOST {url.path} HTTP/1.1'
        authorization = self._create_signature(host, date, signature_origin)
        
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Host': host,
            'Date': date,
            'Authorization': authorization
        }

    async def verify_face(self, image1_base64, image2_base64):
        """比对两张人脸图片
        
        Args:
            image1_base64: 证件照的Base64编码
            image2_base64: 现场拍摄照片的Base64编码
            
        Returns:
            dict: 比对结果，包含相似度分数
        """
        try:
            data = {
                "header": {
                    "app_id": self.app_id,
                    "status": 3
                },
                "parameter": {
                    "s67c9c78c": {
                        "face_detect": "1",
                        "face_compare": "1",  # 启用人脸比对
                        "threshold": "0.8"    # 相似度阈值
                    }
                },
                "payload": {
                    "image1": {
                        "image": image1_base64,
                        "encoding": "jpg"
                    },
                    "image2": {
                        "image": image2_base64,
                        "encoding": "jpg"
                    }
                }
            }

            headers = self._prepare_headers(data)
            response = requests.post(self.api_url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                return self._parse_response(result)
            else:
                return {
                    'success': False,
                    'error': f'API request failed with status code: {response.status_code}'
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _parse_response(self, response):
        """解析API响应"""
        try:
            if response.get('header', {}).get('code') != 0:
                return {
                    'success': False,
                    'error': response.get('header', {}).get('message', 'Unknown error')
                }

            result = response.get('payload', {}).get('result', {})
            face_compare = result.get('face_compare', {})
            
            # 提取比对结果
            return {
                'success': True,
                'score': face_compare.get('score', 0),  # 相似度分数
                'is_same_person': face_compare.get('score', 0) >= 0.8,  # 是否为同一人
                'face1_detected': bool(result.get('face1_detection', {}).get('faces')),
                'face2_detected': bool(result.get('face2_detection', {}).get('faces'))
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to parse response: {str(e)}'
            }

    def verify_identity(self, id_photo_base64, live_photo_base64):
        """验证身份（同步版本）
        
        Args:
            id_photo_base64: 证件照的Base64编码
            live_photo_base64: 现场拍摄照片的Base64编码
            
        Returns:
            dict: 验证结果
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.verify_face(id_photo_base64, live_photo_base64))
            return result
        finally:
            loop.close() 