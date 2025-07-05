import base64
import hashlib
import hmac
import json
import time
import requests
from datetime import datetime
from flask import current_app
from urllib.parse import urlparse, urlencode
import asyncio
import os
from wsgiref.handlers import format_date_time
from time import mktime
from typing import Tuple
from app.config import Config

class FaceRecognitionService:
    """科大讯飞人脸识别服务
    
    提供人脸检测、表情分析等功能
    """
    
    def __init__(self):
        """初始化服务，写死API凭证"""
        self.appid = 'af632c9a'
        self.apikey = '0f38b7916bc3ee000443a308b1d0d8da'
        self.apisecret = 'ZGY3MGMyZjM1NjhjNjU3MzU3ZWQ0MDMw'
        self.server_id = 's67c9c78c'
        self.host = 'api.xf-yun.com'
        self.url = f'https://{self.host}/v1/private/{self.server_id}'

    def _create_auth_url(self, method="POST"):
        """生成带鉴权信息的URL"""
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        
        # 生成签名原文
        signature_origin = f"host: {self.host}\ndate: {date}\n{method} /v1/private/{self.server_id} HTTP/1.1"
        
        # 生成签名
        signature_sha = hmac.new(
            self.apisecret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode('utf-8')
        
        # 组装 authorization
        authorization_origin = f'api_key="{self.apikey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')
        
        # 组装查询参数
        values = {
            "host": self.host,
            "date": date,
            "authorization": authorization
        }
        
        return self.url + "?" + urlencode(values)

    def _prepare_body(self, id_photo_data: bytes, live_photo_data: bytes) -> str:
        """准备请求体"""
        body = {
            "header": {
                "app_id": self.appid,
                "status": 3
            },
            "parameter": {
                self.server_id: {
                    "service_kind": "face_compare",
                    "face_compare_result": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            },
            "payload": {
                "input1": {
                    "encoding": "jpg",
                    "status": 3,
                    "image": base64.b64encode(id_photo_data).decode('utf-8')
                },
                "input2": {
                    "encoding": "jpg",
                    "status": 3,
                    "image": base64.b64encode(live_photo_data).decode('utf-8')
                }
            }
        }
        return json.dumps(body)

    def verify_face(self, id_photo_data: bytes, live_photo_data: bytes) -> Tuple[bool, float, str]:
        """
        验证两张人脸照片是否为同一个人
        
        Args:
            id_photo_data: 证件照片的二进制数据
            live_photo_data: 实时照片的二进制数据
            
        Returns:
            Tuple[bool, float, str]: (是否为同一人, 相似度, 错误信息)
        """
        try:
            # 准备请求URL和请求体
            request_url = self._create_auth_url()
            request_body = self._prepare_body(id_photo_data, live_photo_data)
            
            # 准备请求头
            headers = {
                'Content-Type': "application/json",
                'Accept': "application/json",
                'host': self.host,
                'app_id': self.appid
            }
            
            # 发送请求
            response = requests.post(request_url, data=request_body, headers=headers)
            resp_data = json.loads(response.content.decode('utf-8'))
            
            # 解析结果
            if 'payload' in resp_data and 'face_compare_result' in resp_data['payload']:
                result = json.loads(
                    base64.b64decode(resp_data['payload']['face_compare_result']['text']).decode()
                )
                
                # 获取相似度得分
                score = float(result.get('score', 0))
                
                # 判断是否为同一人（相似度大于0.9）
                is_same_person = score > 0.9
                
                return is_same_person, score, ""
            else:
                error_msg = resp_data.get('message', '人脸比对失败')
                return False, 0.0, error_msg
                
        except Exception as e:
            error_msg = f"人脸验证出错: {str(e)}"
            return False, 0.0, error_msg

    def _create_signature(self, host, date, signature_origin):
        """生成请求签名
        
        Args:
            host: API主机地址
            date: 当前UTC时间
            signature_origin: 原始签名字符串
            
        Returns:
            str: Base64编码的授权字符串
        """
        signature_sha = hmac.new(
            self.apisecret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = f'api_key="{self.apikey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        return authorization

    def _prepare_headers(self, data):
        """准备HTTP请求头
        
        Args:
            data: 请求数据
            
        Returns:
            dict: 包含所有必要头部的字典
        """
        url = urlparse(self.url)
        host = url.netloc
        date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        signature_origin = f'host: {host}\ndate: {date}\nPOST {url.path} HTTP/1.1'
        authorization = self._create_signature(host, date, signature_origin)
        
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Host': host,
            'Date': date,
            'Authorization': authorization,
            'app_id': self.appid  # 添加 app_id 头部
        }

    async def analyze_face(self, image_base64):
        """分析人脸表情和状态
        
        Args:
            image_base64: Base64编码的图片数据
            
        Returns:
            dict: 包含分析结果的字典，格式如下：
            {
                'success': bool,
                'faces': [
                    {
                        'location': dict,  # 脸部位置
                        'attributes': {     # 脸部属性
                            'age': int,
                            'gender': str,
                            'expression': str,
                            'emotion': str,
                            'glasses': str
                        }
                    }
                ]
            }
        """
        try:
            data = {
                "header": {
                    "app_id": self.appid,
                    "status": 3
                },
                "parameter": {
                    "s67c9c78c": {
                        "face_detect": "1",
                        "face_compare": "0"
                    }
                },
                "payload": {
                    "image1": {
                        "image": image_base64,
                        "encoding": "jpg"
                    }
                }
            }

            headers = self._prepare_headers(data)
            response = requests.post(self.url, headers=headers, json=data)
            
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
        """解析API响应
        
        Args:
            response: API返回的JSON响应
            
        Returns:
            dict: 解析后的结果
        """
        try:
            if response.get('header', {}).get('code') != 0:
                return {
                    'success': False,
                    'error': response.get('header', {}).get('message', 'Unknown error')
                }

            result = response.get('payload', {}).get('result', {})
            face_data = result.get('face_detection', {})

            faces = []
            for face in face_data.get('faces', []):
                face_info = {
                    'location': face.get('location', {}),
                    'attributes': {
                        'age': face.get('attributes', {}).get('age', {}).get('value'),
                        'gender': face.get('attributes', {}).get('gender', {}).get('value'),
                        'expression': face.get('attributes', {}).get('expression', {}).get('value'),
                        'emotion': face.get('attributes', {}).get('emotion', {}).get('value'),
                        'glasses': face.get('attributes', {}).get('glasses', {}).get('value'),
                    }
                }
                faces.append(face_info)

            return {
                'success': True,
                'faces': faces
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to parse response: {str(e)}'
            }

    def get_face_attributes(self, image_base64):
        """获取人脸属性（同步版本）
        
        Args:
            image_base64: Base64编码的图片数据
            
        Returns:
            dict: 包含人脸属性的字典
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.analyze_face(image_base64))
            return result
        finally:
            loop.close() 