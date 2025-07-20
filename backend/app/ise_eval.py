import websocket, json, base64, threading, time, ssl, requests, io, os
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from datetime import datetime, timezone
from pydub import AudioSegment
import xml.etree.ElementTree as ET
import hmac, hashlib

APP_ID = "e5850021"
API_KEY = "dda0f69489a3db1e0d495f40a5fd40eb"
API_SECRET = "OTNlMGI0OWUxM2JlMWRhM2EzNDVhZjAw"
ISE_HOST = "wss://ise-api.xfyun.cn/v2/open-ise"

FFMPEG_DIR = r"D:\FFMEPG\ffmpeg-7.0.2-essentials_build\ffmpeg-7.0.2-essentials_build\bin"
os.environ["PATH"] += os.pathsep + FFMPEG_DIR
AudioSegment.converter = os.path.join(FFMPEG_DIR, "ffmpeg.exe")


def gen_ise_ws_url():
    """生成带鉴权的WebSocket URL"""
    now = datetime.now(timezone.utc)
    date_str = format_date_time(now.timestamp())

    sign_origin = f"host: ise-api.xfyun.cn\ndate: {date_str}\nGET /v2/open-ise HTTP/1.1"
    sign_sha = hmac.new(API_SECRET.encode(), sign_origin.encode(), hashlib.sha256).digest()
    sign_b64 = base64.b64encode(sign_sha).decode()

    auth_origin = f'api_key="{API_KEY}", algorithm="hmac-sha256", headers="host date request-line", signature="{sign_b64}"'
    auth_b64 = base64.b64encode(auth_origin.encode()).decode()

    qs = urlencode({"authorization": auth_b64, "date": date_str, "host": "ise-api.xfyun.cn"})
    return f"{ISE_HOST}?{qs}", date_str


def process_audio(audio_path: str) -> bytes:
    """
    处理音频文件，确保符合讯飞要求
    :param audio_path: 音频文件路径或URL
    :return: 转换后的MP3字节流
    """
    print("[ISE] ▶ 处理音频:", audio_path)

    # 下载或读取音频文件
    if audio_path.startswith(('http://', 'https://')):
        print("[ISE] ▶ 下载远程音频")
        response = requests.get(audio_path, timeout=15)
        response.raise_for_status()
        raw = response.content
    else:
        print("[ISE] ▶ 读取本地音频文件")
        with open(audio_path, 'rb') as f:
            raw = f.read()

    print("[ISE] ▶ 原始音频大小(bytes):", len(raw))

    # 获取文件扩展名
    ext = os.path.splitext(audio_path)[1].lower().lstrip('.')

    # 特殊处理webm格式
    if ext == 'webm':
        audio = AudioSegment.from_file(io.BytesIO(raw), format="webm", codec="opus")
    else:
        audio = AudioSegment.from_file(io.BytesIO(raw), format=ext)

    # 标准化音频参数
    audio = audio.set_frame_rate(16000).set_channels(1)

    # 如果音频太短，添加静音
    if len(audio) < 500:  # 少于500ms
        silence = AudioSegment.silent(duration=500 - len(audio))
        audio += silence

    # 导出MP3
    buf = io.BytesIO()
    audio.export(buf,
                 format="mp3",
                 bitrate="16k",
                 codec="libmp3lame",
                 parameters=[
                     "-ar", "16000",
                     "-ac", "1",
                     "-acodec", "libmp3lame",
                     "-b:a", "16k",
                     "-write_xing", "0",
                     "-id3v2_version", "0"
                 ])

    mp3_data = buf.getvalue()
    print("[ISE] ▶ 转码完成 mp3 大小(bytes):", len(mp3_data))
    print("[ISE] ▶ mp3前5字节:", mp3_data[:5])
    return mp3_data


def parse_ise_xml(xml_str):
    """解析评测结果XML"""
    try:
        root = ET.fromstring(xml_str)
        chapter = root.find(".//read_chapter")
        if chapter is None:
            return {}
        return {
            "accuracy_score": chapter.attrib.get("accuracy_score"),
            "fluency_score": chapter.attrib.get("fluency_score"),
            "integrity_score": chapter.attrib.get("integrity_score"),
            "total_score": chapter.attrib.get("total_score"),
            "standard_score": chapter.attrib.get("standard_score"),
        }
    except Exception as e:
        print("[ISE] 解析XML出错:", e)
        return {}


def ise_eval(audio_path: str, eval_text: str, timeout=90):
    """
    语音评测函数
    :param audio_path: 音频文件路径或URL
    :param eval_text: 要评测的文本
    :param timeout: 超时时间(秒)
    :return: (xml结果, 评分字典)
    :raises RuntimeError: 评测失败时抛出异常
    """
    ws_url, date_header = gen_ise_ws_url()
    mp3_audio = process_audio(audio_path)

    holder = {"xml": None, "error": None, "code": None, "message": None}

    def on_open(ws):
        print("[ISE] WS opened, sending init frame...")

        # 初始化帧必须包含cmd参数
        init_frame = {
            "common": {"app_id": APP_ID},
            "business": {
                "cmd": "ssb",  # 关键参数
                "category": "read_sentence",
                "sub": "ise",
                "ent": "cn_vip",  # 英语评测
                "aue": "lame",
                "text": '\uFEFF' + "[content]\n" + eval_text,
                "rstcd": "utf8"
            },
            "data": {"status": 0}
        }
        ws.send(json.dumps(init_frame))
        print("[ISE] init frame sent.")

        # 发送音频数据
        CHUNK = 1280
        for idx in range(0, len(mp3_audio), CHUNK):
            chunk = mp3_audio[idx:idx + CHUNK]
            frame = {
                "business": {
                    "cmd": "auw",
                    "aus": 2,  # 音频数据中段
                    "aue": "lame"
                },
                "data": {
                    "status": 1,
                    "data": base64.b64encode(chunk).decode(),
                    "encoding": "raw"
                }
            }
            ws.send(json.dumps(frame))
            time.sleep(0.04)  # 控制发送速率

        # 发送结束帧
        end_frame = {
            "business": {
                "cmd": "auw",
                "aus": 4,  # 音频结束
                "aue": "lame"
            },
            "data": {"status": 2}
        }
        ws.send(json.dumps(end_frame))
        print("[ISE] end frame sent.")

    def on_message(ws, message):
        print("[ISE] Message received:", message)
        msg_json = json.loads(message)

        # 记录错误信息
        if "code" in msg_json and msg_json["code"] != 0:
            holder["code"] = msg_json.get("code")
            holder["message"] = msg_json.get("message")
            holder["error"] = f"code={holder['code']} message={holder['message']}"
            ws.close()
            return

        # 处理最终结果
        if msg_json.get("data", {}).get("status") == 2:
            xml_base64 = msg_json["data"].get("data")
            if xml_base64:
                xml_str = base64.b64decode(xml_base64).decode()
                holder["xml"] = xml_str

                # 解析xml并打印评分（模仿示例代码格式）
                try:
                    root = ET.fromstring(xml_str)
                    read_chapter = root.find(".//read_chapter")
                    if read_chapter is not None:
                        accuracy_score = read_chapter.attrib.get("accuracy_score")
                        fluency_score = read_chapter.attrib.get("fluency_score")
                        total_score = read_chapter.attrib.get("total_score")
                        standard_score = read_chapter.attrib.get("standard_score")

                        print("\n🔍 提取评分结果：")
                        print(f"✅ accuracy_score: {accuracy_score}")
                        print(f"✅ fluency_score: {fluency_score}")
                        print(f"✅ total_score: {total_score}")
                        print(f"✅ standard_score: {standard_score}")
                    else:
                        print("⚠️ 未找到 read_chapter 节点")
                except Exception as e:
                    print("❌ 解析 XML 出错:", e)
            ws.close()

    def on_error(ws, error):
        print("[ISE] WS error:", error)
        holder["error"] = str(error)
        ws.close()

    def on_close(ws, *args):
        print("[ISE] WS closed")

    # 创建WebSocket连接
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(
        ws_url,
        header=[f"Date: {date_header}"],
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    # 启动线程运行WebSocket
    thread = threading.Thread(target=ws.run_forever, kwargs={
        "sslopt": {"cert_reqs": ssl.CERT_NONE},
        "ping_interval": 30,
        "ping_timeout": 10
    })
    thread.start()

    # 等待结果
    waited = 0
    while waited < timeout:
        if holder["xml"] or holder["error"]:
            break
        time.sleep(1)
        waited += 1

    thread.join(2)

    # 处理结果
    if holder["error"]:
        raise RuntimeError(holder["error"])
    if not holder["xml"]:
        raise RuntimeError("ISE evaluation timeout or no result")

    scores = parse_ise_xml(holder["xml"])
    print("[ISE] Scores parsed:", scores)
    return holder["xml"], scores