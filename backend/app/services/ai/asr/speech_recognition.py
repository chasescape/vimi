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

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class SpeechRecognition:
    def __init__(self, app_id, api_key, api_secret):
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.result_text = ""
        self.is_completed = False
        self.error_message = ""

    def recognize_audio_file(self, audio_file_path):
        """
        识别音频文件并返回识别结果
        """
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"音频文件不存在: {audio_file_path}")

        self.result_text = ""
        self.is_completed = False
        self.error_message = ""

        print(f"开始语音识别，文件: {audio_file_path}")
        print(f"文件大小: {os.path.getsize(audio_file_path)} bytes")

        try:
            ws_param = Ws_Param(
                APPID=self.app_id,
                APIKey=self.api_key,
                APISecret=self.api_secret,
                AudioFile=audio_file_path
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
            
            # 运行WebSocket连接，设置超时
            import threading
            import time
            
            # 在单独的线程中运行WebSocket
            ws_thread = threading.Thread(target=lambda: ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}))
            ws_thread.daemon = True
            ws_thread.start()
            
            # 等待识别完成或超时
            timeout = 30  # 30秒超时
            start_time = time.time()
            
            while not self.is_completed and (time.time() - start_time) < timeout:
                time.sleep(0.1)
            
            if not self.is_completed:
                self.error_message = "识别超时"
                print("识别超时")
            
            print(f"识别完成，结果: {self.result_text}")
            print(f"是否完成: {self.is_completed}")
            print(f"错误信息: {self.error_message}")
            
            return {
                'success': self.is_completed and not self.error_message and self.result_text.strip(),
                'text': self.result_text,
                'error': self.error_message
            }
        except Exception as e:
            print(f"语音识别异常: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'text': '',
                'error': f'语音识别异常: {str(e)}'
            }

    def _on_message(self, ws, message):
        """处理WebSocket消息"""
        try:
            print(f"收到WebSocket消息: {message[:200]}...")  # 只显示前200个字符
            data = json.loads(message)
            code = data.get("code")
            sid = data.get("sid")
            
            print(f"消息代码: {code}, SID: {sid}")
            
            if code != 0:
                err_msg = data.get("message", "未知错误")
                self.error_message = f"识别错误: {err_msg}"
                print(f"sid:{sid} call error:{err_msg} code is:{code}")
            else:
                result_data = data.get("data", {}).get("result", {}).get("ws", [])
                print(f"识别数据: {result_data}")
                if result_data:
                    result = ""
                    for i in result_data:
                        for w in i.get("cw", []):
                            result += w.get("w", "")
                    self.result_text += result
                    print(f"sid:{sid} 识别结果: {result}")
                else:
                    print("没有识别到文本内容")
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

    def _on_open(self, ws, ws_param):
        """处理WebSocket连接建立"""
        print("### WebSocket连接已建立，开始发送音频数据")
        def run(*args):
            frame_size = 8000  # 每一帧的音频大小
            interval = 0.04  # 发送音频间隔(单位:s)
            status = STATUS_FIRST_FRAME  # 音频的状态信息

            try:
                with open(ws_param.AudioFile, "rb") as fp:
                    frame_count = 0
                    while True:
                        buf = fp.read(frame_size)
                        frame_count += 1
                        # 文件结束
                        if not buf:
                            status = STATUS_LAST_FRAME
                            print(f"发送最后一帧，总帧数: {frame_count}")
                        
                        # 第一帧处理
                        if status == STATUS_FIRST_FRAME:
                            print(f"发送第一帧，帧大小: {len(buf)} bytes")
                            d = {
                                "common": ws_param.CommonArgs,
                                "business": ws_param.BusinessArgs,
                                "data": {
                                    "status": 0,
                                    "format": "audio/L16;rate=16000",
                                    "audio": str(base64.b64encode(buf), 'utf-8'),
                                    "encoding": "raw"
                                }
                            }
                            d = json.dumps(d)
                            ws.send(d)
                            status = STATUS_CONTINUE_FRAME
                        
                        # 中间帧处理
                        elif status == STATUS_CONTINUE_FRAME:
                            if frame_count % 100 == 0:  # 每100帧打印一次进度
                                print(f"发送第 {frame_count} 帧")
                            d = {
                                "data": {
                                    "status": 1,
                                    "format": "audio/L16;rate=16000",
                                    "audio": str(base64.b64encode(buf), 'utf-8'),
                                    "encoding": "raw"
                                }
                            }
                            ws.send(json.dumps(d))
                        
                        # 最后一帧处理
                        elif status == STATUS_LAST_FRAME:
                            print("发送结束帧")
                            d = {
                                "data": {
                                    "status": 2,
                                    "format": "audio/L16;rate=16000",
                                    "audio": str(base64.b64encode(buf), 'utf-8'),
                                    "encoding": "raw"
                                }
                            }
                            ws.send(json.dumps(d))
                            time.sleep(1)
                            break
                        
                        # 模拟音频采样间隔
                        time.sleep(interval)
                ws.close()
            except Exception as e:
                print(f"发送音频数据时发生异常: {str(e)}")
                import traceback
                traceback.print_exc()
                ws.close()

        thread.start_new_thread(run, ())


class Ws_Param(object):
    """WebSocket参数类"""
    def __init__(self, APPID, APIKey, APISecret, AudioFile):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.AudioFile = AudioFile

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {
            "domain": "iat",
            "language": "zh_cn",
            "accent": "mandarin",
            "vinfo": 1,
            "vad_eos": 10000
        }

    def create_url(self):
        """生成WebSocket URL"""
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        
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
            "host": "ws-api.xfyun.cn"
        }
        
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        return url 