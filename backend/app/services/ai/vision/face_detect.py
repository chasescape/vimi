import base64
import hashlib
import hmac
import json
import time
import requests
from datetime import datetime
from flask import current_app
from urllib.parse import urlencode, urlparse
import asyncio
from wsgiref.handlers import format_date_time
from time import mktime

class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg

class Url:
    def __init__(self, host, path, schema):
        self.host = host
        self.path = path
        self.schema = schema

class FaceDetectService:
    """科大讯飞人脸检测服务
    
    提供人脸检测、表情分析等功能
    """
    
    # 表情映射
    EXPRESSION_MAP = {
        0: "惊讶",
        1: "害怕",
        2: "厌恶",
        3: "高兴",
        4: "悲伤",
        5: "生气",
        6: "正常"
    }

    # 性别映射
    GENDER_MAP = {
        0: "男性",
        1: "女性"
    }

    # 眼镜映射
    GLASS_MAP = {
        0: "不戴眼镜",
        1: "戴眼镜"
    }

    # 发型映射
    HAIR_MAP = {
        0: "光头",
        1: "短发",
        2: "长发"
    }

    # 胡须映射
    BEARD_MAP = {
        0: "没有胡子",
        1: "有胡子"
    }

    # 口罩映射
    MASK_MAP = {
        0: "没戴口罩",
        1: "戴口罩"
    }
    
    def __init__(self):
        """初始化服务"""
        self.appid = 'af632c9a'
        self.apikey = '0f38b7916bc3ee000443a308b1d0d8da'
        self.apisecret = 'ZGY3MGMyZjM1NjhjNjU3MzU3ZWQ0MDMw'
        self.server_id = 's67c9c78c'
        self.host = 'api.xf-yun.com'

    def _parse_url(self, request_url):
        """解析URL"""
        stidx = request_url.index("://")
        host = request_url[stidx + 3:]
        schema = request_url[:stidx + 3]
        edidx = host.index("/")
        if edidx <= 0:
            raise AssembleHeaderException("invalid request url:" + request_url)
        path = host[edidx:]
        host = host[:edidx]
        return Url(host, path, schema)

    def _assemble_ws_auth_url(self, request_url, method="POST", api_key="", api_secret=""):
        """生成带鉴权信息的URL"""
        u = self._parse_url(request_url)
        host = u.host
        path = u.path
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 生成签名原文
        signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
        print("签名原文:", signature_origin)

        # 生成签名
        signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                               digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        # 组装authorization
        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            api_key, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 组装查询参数
        values = {
            "host": host,
            "date": date,
            "authorization": authorization
        }

        return request_url + "?" + urlencode(values)

    def _gen_body(self, image_base64):
        """生成请求体"""
        body = {
            "header": {
                "app_id": self.appid,
                "status": 3
            },
            "parameter": {
                self.server_id: {
                    "service_kind": "face_detect",
                    "detect_points": "1",  # 检测特征点
                    "detect_property": "1",  # 检测人脸属性
                    "face_detect_result": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            },
            "payload": {
                "input1": {
                    "encoding": "jpg",
                    "image": image_base64,
                    "status": 3
                }
            }
        }
        return json.dumps(body)

    def analyze_face(self, image_base64):
        """分析人脸"""
        try:
            # 准备URL和认证信息
            url = f'http://{self.host}/v1/private/{self.server_id}'
            request_url = self._assemble_ws_auth_url(url, "POST", self.apikey, self.apisecret)
            
            # 准备请求头
            headers = {
                'content-type': "application/json",
                'host': self.host,
                'app_id': self.appid
            }
            
            print("\n发送人脸检测请求:")
            print(f"请求URL: {request_url}")
            print(f"图片大小: {len(image_base64)/1024:.2f}KB")
            print(f"请求头: {headers}")
            
            # 准备请求体
            body = self._gen_body(image_base64)
            
            # 发送请求
            response = requests.post(request_url, data=body, headers=headers)
            
            print(f"\n响应状态码: {response.status_code}")
            if response.status_code != 200:
                print(f"错误响应内容: {response.text}")
                return {
                    'success': False,
                    'error': f'API request failed with status code: {response.status_code}. Response: {response.text}'
                }
            
            resp_data = response.json()
            print(f"\n响应数据:")
            print(json.dumps(resp_data, indent=2, ensure_ascii=False))
            
            if resp_data['header']['code'] != 0:
                error_msg = resp_data['header'].get('message', '未知错误')
                print(f"\nAPI错误: {error_msg}")
                return {
                    'success': False,
                    'error': error_msg
                }

            # 解析结果
            result_text = resp_data['payload']['face_detect_result']['text']
            result = json.loads(base64.b64decode(result_text).decode())
            print(f"\n解析后的结果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            face_num = result.get('face_num', 0)
            faces = []
            
            for i in range(1, face_num + 1):
                face_key = f'face_{i}'
                if face_key in result:
                    face = result[face_key]
                    face_info = {
                        'score': face['score'] * 100,  # 转换为百分比
                        'location': {
                            'x': face['x'],
                            'y': face['y'],
                            'width': face['w'],
                            'height': face['h']
                        }
                    }
                    
                    # 添加人脸属性
                    if 'property' in face:
                        face_info['properties'] = self._parse_face_properties(face['property'])
                        
                    faces.append(face_info)

            final_result = {
                'success': True,
                'face_count': face_num,
                'faces': faces
            }
            return final_result

        except Exception as e:
            print(f"\n发生异常: {str(e)}")
            import traceback
            print(f"详细错误: {traceback.format_exc()}")
            return {
                'success': False,
                'error': str(e)
            }

    def _parse_face_properties(self, properties):
        """解析人脸属性"""
        return {
            "expression": self.EXPRESSION_MAP.get(properties.get("expression", 6), "未知"),
            "gender": self.GENDER_MAP.get(properties.get("gender", -1), "未知"),
            "glass": self.GLASS_MAP.get(properties.get("glass", -1), "未知"),
            "hair": self.HAIR_MAP.get(properties.get("hair", -1), "未知"),
            "beard": self.BEARD_MAP.get(properties.get("beard", -1), "未知"),
            "mask": self.MASK_MAP.get(properties.get("mask", -1), "未知")
        } 