# -*- coding:utf-8 -*-

import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os

#本demo示例是单次上传文本的示例，如果用在对时效要求高的交互场景，需要流式上传文本
# STATUS_FIRST_FRAME = 0  # 第一帧的标识
# STATUS_CONTINUE_FRAME = 1  # 中间帧标识
# STATUS_LAST_FRAME = 2  # 最后一帧的标识

class TextToSpeech:
    def __init__(self, app_id, api_key, api_secret):
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.audio_data = b""
        self.is_completed = False
        self.error_message = ""
        self.audio_file_path = ""

    def synthesize_text(self, text, output_file_path=None):
        """
        将文本转换为语音并保存到文件
        """
        if not text or not text.strip():
            raise ValueError("文本内容不能为空")

        self.audio_data = b""
        self.is_completed = False
        self.error_message = ""
        
        # 如果没有指定输出文件路径，使用默认路径
        if not output_file_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file_path = f"uploads/synthesized_{timestamp}.mp3"
        
        self.audio_file_path = output_file_path
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        print(f"开始文字转语音，文本: {text[:50]}...")
        print(f"输出文件: {output_file_path}")

        try:
            ws_param = Ws_Param(
                APPID=self.app_id,
                APIKey=self.api_key,
                APISecret=self.api_secret,
                Text=text
            )

            websocket.enableTrace(True)  # 启用WebSocket调试
            ws_url = ws_param.create_url()
            
            print(f"WebSocket URL: {ws_url}")
            
            # 创建WebSocket连接
            ws = websocket.WebSocketApp(
                ws_url,
                on_message=lambda ws, msg: self._on_message(ws, msg),
                on_error=lambda ws, err: self._on_error(ws, err),
                on_close=lambda ws, code, msg: self._on_close(ws, code, msg)
            )
            ws.on_open = lambda ws: self._on_open(ws, ws_param)
            
            # 在单独的线程中运行WebSocket
            import threading
            
            ws_thread = threading.Thread(target=lambda: ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}))
            ws_thread.daemon = True
            ws_thread.start()
            
            # 等待合成完成或超时
            timeout = 30  # 30秒超时
            start_time = time.time()
            
            while not self.is_completed and (time.time() - start_time) < timeout:
                time.sleep(0.1)
            
            if not self.is_completed:
                self.error_message = "合成超时"
                print("合成超时")
            
            print(f"合成完成，文件: {self.audio_file_path}")
            print(f"是否完成: {self.is_completed}")
            print(f"错误信息: {self.error_message}")
            
            # 检查音频文件是否成功生成
            audio_file_exists = os.path.exists(self.audio_file_path)
            audio_file_size = os.path.getsize(self.audio_file_path) if audio_file_exists else 0
            
            # 如果音频文件存在且不为空，则认为成功
            success = audio_file_exists and audio_file_size > 0
            
            return {
                'success': success,
                'audio_file_path': self.audio_file_path,
                'error': self.error_message if not success else ""
            }
        except Exception as e:
            print(f"文字转语音异常: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'audio_file_path': '',
                'error': f'文字转语音异常: {str(e)}'
            }

    def _on_message(self, ws, message):
        """处理WebSocket消息"""
        try:
            print(f"收到WebSocket消息: {message[:200]}...")  # 只显示前200个字符
            data = json.loads(message)
            code = data.get("header", {}).get("code")
            sid = data.get("header", {}).get("sid")
            
            print(f"消息代码: {code}, SID: {sid}")
            
            if code != 0:
                err_msg = data.get("message", "未知错误")
                self.error_message = f"合成错误: {err_msg}"
                print(f"sid:{sid} call error:{err_msg} code is:{code}")
            else:
                # 处理音频数据
                if "payload" in data and "audio" in data["payload"]:
                    audio = data["payload"]["audio"]["audio"]
                    audio_bytes = base64.b64decode(audio)
                    self.audio_data += audio_bytes
                    
                    status = data["payload"]["audio"]["status"]
                    print(f"收到音频数据，状态: {status}, 大小: {len(audio_bytes)} bytes")
                    
                    if status == 2:  # 最后一帧
                        print("收到最后一帧，保存音频文件")
                        with open(self.audio_file_path, 'wb') as f:
                            f.write(self.audio_data)
                        self.is_completed = True
                        ws.close()
                else:
                    print("消息中没有音频数据")
        except Exception as e:
            self.error_message = f"解析消息异常: {str(e)}"
            print(f"receive msg,but parse exception: {e}")
            import traceback
            traceback.print_exc()

    def _on_error(self, ws, error):
        """处理WebSocket错误"""
        self.error_message = f"WebSocket错误: {str(error)}"
        print(f"### WebSocket错误: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        """处理WebSocket关闭"""
        self.is_completed = True
        print(f"### WebSocket连接已关闭，状态码: {close_status_code}, 消息: {close_msg}")
        
        # 检查音频文件是否成功生成
        if os.path.exists(self.audio_file_path):
            file_size = os.path.getsize(self.audio_file_path)
            if file_size > 0:
                print(f"✅ 音频文件生成成功，大小: {file_size} bytes")
                # 清除错误信息，因为音频文件已成功生成
                self.error_message = ""
            else:
                print("❌ 音频文件为空")
        else:
            print("❌ 音频文件未生成")

    def _on_open(self, ws, ws_param):
        """处理WebSocket连接建立"""
        print("### WebSocket连接已建立，开始发送文本数据")
        def run(*args):
            try:
                d = {
                    "header": ws_param.CommonArgs,
                    "parameter": ws_param.BusinessArgs,
                    "payload": ws_param.Data,
                }
                d = json.dumps(d)
                print("------>开始发送文本数据")
                ws.send(d)
                
                # 清理之前的音频文件
                if os.path.exists(self.audio_file_path):
                    os.remove(self.audio_file_path)
                    
            except Exception as e:
                print(f"发送文本数据时发生异常: {str(e)}")
                import traceback
                traceback.print_exc()
                ws.close()

        thread.start_new_thread(run, ())

        
class Ws_Param(object):
    """WebSocket参数类"""
    def __init__(self, APPID, APIKey, APISecret, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID, "status": 2}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {
        "tts": {
            "vcn": "x5_lingfeiyi_flow",  # 发音人参数，更换不同的发音人会有不同的音色效果
                "volume": 50,    # 设置音量大小
                "rhy": 0,   # 是否返回拼音标注 0:不返回拼音, 1:返回拼音（纯文本格式，utf8编码）
                "speed": 50,    # 设置合成语速，值越大，语速越快
                "pitch": 50,    # 设置振幅高低，可通过该参数调整效果
                "bgs": 0,   # 背景音 0:无背景音, 1:内置背景音1, 2:内置背景音2
                "reg": 0,   # 英文发音方式 0:自动判断处理，如果不确定将按照英文词语拼写处理（缺省）, 1:所有英文按字母发音, 2:自动判断处理，如果不确定将按照字母朗读
                "rdn": 0,   # 合成音频数字发音方式 0:自动判断, 1:完全数值, 2:完全字符串, 3:字符串优先
            "audio": {
                    "encoding": "lame",  # 合成音频格式， lame 合成音频格式为mp3
                    "sample_rate": 24000,  # 合成音频采样率， 16000, 8000, 24000
                "channels": 1,  # 音频声道数
                    "bit_depth": 16, # 合成音频位深 ：16, 8
                "frame_size": 0
            }
        }
    }
        
        self.Data = {
        "text": {
            "encoding": "utf8",
            "compress": "raw",
            "format": "plain",
            "status": 2,
            "seq": 0,
            "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")   # 待合成文本base64格式
        }
        }

    def create_url(self):
        """生成WebSocket URL"""
        url = 'wss://cbm01.cn-huabei-1.xf-yun.com/v1/private/mcd9m97e6'
        
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "cbm01.cn-huabei-1.xf-yun.com" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v1/private/mcd9m97e6 " + "HTTP/1.1"
        
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(
            self.APISecret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = 'api_key="%s", algorithm="%s", headers="%s", signature="%s"' % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha
        )
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "cbm01.cn-huabei-1.xf-yun.com"
        }
        
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        return url


class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg


class Url:
    def __init__(this, host, path, schema):
        this.host = host
        this.path = path
        this.schema = schema
        pass


# calculate sha256 and encode to base64
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


# build websocket auth request url
def assemble_ws_auth_url(requset_url, method="GET", api_key="", api_secret=""):
    u = parse_url(requset_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    print(date)
    # date = "Thu, 12 Dec 2019 01:57:27 GMT"
    signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
    # print(signature_origin)
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
        api_key, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    # print(authorization_origin)
    values = {
        "host": host,
        "date": date,
        "authorization": authorization
    }

    return requset_url + "?" + urlencode(values)


if __name__ == "__main__":
    # 从控制台页面获取以下密钥信息，控制台地址：https://console.xfyun.cn/app/myapp
    appid = 'ea0e453f'
    apikey = 'cfe0b8933be42c3dfcf6e1d3e2f2882e'
    apisecret = 'ZWI5NGJhOGJmZGQ5ZDM5MTU0ZWExMGVk'

    text_to_speech = TextToSpeech(app_id=appid, api_key=apikey, api_secret=apisecret)
    result = text_to_speech.synthesize_text("全红婵，2007年3月28日出生于广东省湛江市，中国国家跳水队女运动员，主项为女子10米跳台。")
    print(f"合成结果: {result}")
