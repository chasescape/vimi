import websocket, _thread as thread, json, ssl, time, hmac, hashlib, base64
from urllib.parse import urlparse, urlencode
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime

APPID      = "e5850021"
API_KEY    = "dda0f69489a3db1e0d495f40a5fd40eb"
API_SECRET = "OTNlMGI0OWUxM2JlMWRhM2EzNDVhZjAw"
DOMAIN     = "x1"
SPARK_URL  = "wss://spark-api.xf-yun.com/v1/x1"

def ask_spark_model(user_text: str) -> str:
    result = {"answer": "", "done": False}

    class WsParam:
        def create_url(self):
            host, path = urlparse(SPARK_URL).netloc, urlparse(SPARK_URL).path
            date = format_date_time(mktime(datetime.now().timetuple()))
            sig = f"host: {host}\ndate: {date}\nGET {path} HTTP/1.1"
            sig_h = hmac.new(API_SECRET.encode(), sig.encode(), hashlib.sha256).digest()
            sig_b = base64.b64encode(sig_h).decode()
            auth = base64.b64encode(f'api_key="{API_KEY}", algorithm="hmac-sha256", headers="host date request-line", signature="{sig_b}"'.encode()).decode()
            url = SPARK_URL + "?" + urlencode({"authorization": auth, "date": date, "host": host})
            return url

    def on_open(ws):
        def run(*_):
            prompt = (
                "请对以下文本进行情感分析，只返回 JSON，格式为数字百分比（不带%符号）："
                '{"positive":数字,"neutral":数字,"negative":数字}。\n'
                f"文本：{user_text}"
            )
            data = {
                "header": {"app_id": APPID, "uid": "1"},
                "parameter": {"chat": {"domain": DOMAIN, "temperature": 0.9, "max_tokens": 2048}},
                "payload": {"message": {"text": [{"role": "user", "content": prompt}]}}
            }
            ws.send(json.dumps(data))
        thread.start_new_thread(run, ())

    def on_msg(ws, msg):
        data = json.loads(msg)
        if data["header"]["code"] != 0:
            result["done"] = True
            ws.close()
            return
        txt = data["payload"]["choices"]["text"][0].get("content", "")
        result["answer"] += txt
        if data["payload"]["choices"]["status"] == 2:
            result["done"] = True
            ws.close()

    ws = websocket.WebSocketApp(WsParam().create_url(),
                                on_open=on_open,
                                on_message=on_msg,
                                on_error=lambda *_: None,
                                on_close=lambda *_: None)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    timeout = time.time() + 20
    while not result["done"] and time.time() < timeout:
        time.sleep(0.1)

    return result["answer"]
