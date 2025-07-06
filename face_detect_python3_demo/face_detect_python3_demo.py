#
# 人脸检测和属性分析 WebAPI 接口调用示例
# 运行前：请先填写Appid、APIKey、APISecret以及图片路径
# 运行方法：直接运行 main 即可 
# 结果： 控制台输出结果信息
# 
# 接口文档（必看）：https://www.xfyun.cn/doc/face/xf-face-detect/API.html
#

from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import os
import traceback
import json
import requests

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

class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg


class Url:
    def __init__(this, host, path, schema):
        this.host = host
        this.path = path
        this.schema = schema
        pass


# 进行sha256加密和base64编码
def sha256base64(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    digest = base64.b64encode(sha256.digest()).decode(encoding='utf-8')
    return digest


def parse_url(requset_url):
    stidx = requset_url.index("://")
    host = requset_url[stidx + 3:]
    schema = requset_url[:stidx + 3]
    edidx = host.index("/")
    if edidx <= 0:
        raise AssembleHeaderException("invalid request url:" + requset_url)
    path = host[edidx:]
    host = host[:edidx]
    u = Url(host, path, schema)
    return u


def assemble_ws_auth_url(requset_url, method="GET", api_key="", api_secret=""):
    u = parse_url(requset_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    print(date)
    # date = "Thu, 12 Dec 2019 01:57:27 GMT"
    signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
    print(signature_origin)
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
        api_key, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    print(authorization_origin)
    values = {
        "host": host,
        "date": date,
        "authorization": authorization
    }

    return requset_url + "?" + urlencode(values)

def parse_face_properties(properties):
    """解析人脸属性"""
    result = {
        "expression": EXPRESSION_MAP.get(properties.get("expression", 6), "未知"),
        "gender": GENDER_MAP.get(properties.get("gender", -1), "未知"),
        "glass": GLASS_MAP.get(properties.get("glass", -1), "未知"),
        "hair": HAIR_MAP.get(properties.get("hair", -1), "未知"),
        "beard": BEARD_MAP.get(properties.get("beard", -1), "未知"),
        "mask": MASK_MAP.get(properties.get("mask", -1), "未知")
    }
    return result

def gen_body(appid, img_path, server_id):
    with open(img_path, 'rb') as f:
        img_data = f.read()
    body = {
        "header": {
            "app_id": appid,
            "status": 3
        },
        "parameter": {
            server_id: {
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
                "status": 3,
                "image": str(base64.b64encode(img_data), 'utf-8')
            }
        }
    }
    return json.dumps(body)


def run(appid, apikey, apisecret, img_path, server_id='s67c9c78c'):
    # 检查图片是否存在
    if not os.path.exists(img_path):
        print(f"错误：图片文件不存在: {img_path}")
        return
        
    # 检查图片大小
    file_size = os.path.getsize(img_path)
    print(f"\n图片信息:")
    print(f"- 路径: {img_path}")
    print(f"- 大小: {file_size/1024:.2f} KB")
    
    url = 'http://api.xf-yun.com/v1/private/{}'.format(server_id)
    request_url = assemble_ws_auth_url(url, "POST", apikey, apisecret)
    headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'app_id': appid}
    
    try:
        # 读取并打印图片base64大小
        with open(img_path, 'rb') as f:
            img_data = f.read()
            base64_data = base64.b64encode(img_data)
            print(f"- Base64大小: {len(base64_data)/1024:.2f} KB")
        
        response = requests.post(request_url, data=gen_body(appid, img_path, server_id), headers=headers)
        resp_data = json.loads(response.content.decode('utf-8'))
        
        print("\n响应信息:")
        print(f"- 状态码: {response.status_code}")
        print(f"- 响应头: {response.headers}")
        
        # 解析响应数据
        if resp_data['header']['code'] != 0:
            print("\n请求失败:", resp_data['header'].get('message', '未知错误'))
            return
            
        result = json.loads(base64.b64decode(resp_data['payload']['face_detect_result']['text']).decode())
        print("\n=== 检测结果 ===")
        
        face_num = result.get('face_num', 0)
        if face_num > 0:
            print(f"检测到 {face_num} 张人脸")
            
            # 遍历所有人脸
            for i in range(1, face_num + 1):
                face_key = f'face_{i}'
                if face_key in result:
                    face = result[face_key]
                    print(f"\n人脸 {i}:")
                    print(f"- 置信度: {face['score']*100:.2f}%")
                    
                    # 获取人脸属性
                    if 'property' in face:
                        properties = parse_face_properties(face['property'])
                        print("- 表情:", properties['expression'])
                        print("- 性别:", properties['gender'])
                        print("- 眼镜:", properties['glass'])
                        print("- 发型:", properties['hair'])
                        print("- 胡须:", properties['beard'])
                        print("- 口罩:", properties['mask'])
                    
                    # 获取人脸位置
                    print(f"- 位置: 左上角({face['x']}, {face['y']}), "
                          f"宽度={face['w']}, 高度={face['h']}")
        else:
            print("未检测到人脸")
            
    except Exception as e:
        print(f"\n发生错误: {str(e)}")
        print("详细错误信息:")
        print(traceback.format_exc())

#请填写控制台获取的APPID、APISecret、APIKey以及要检测的图片路径
if __name__ == '__main__':
    run(
        appid='af632c9a',
        apisecret='ZGY3MGMyZjM1NjhjNjU3MzU3ZWQ0MDMw',
        apikey='0f38b7916bc3ee000443a308b1d0d8da',
        img_path=r'D:\whisper\Pictures\Saved Pictures\微信图片_20250706034858.jpg',
    )
