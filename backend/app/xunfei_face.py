# app/utils/xunfei_face.py
import base64, hashlib, hmac, json, requests
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

def gen_face_verify_payload(appid, api_key, api_secret, id_photo_bytes, live_photo_bytes, server_id='s67c9c78c'):
    def sha256base64(data):
        sha256 = hashlib.sha256()
        sha256.update(data)
        return base64.b64encode(sha256.digest()).decode()

    def get_signed_url():
        url = f"http://api.xf-yun.com/v1/private/{server_id}"
        host, path = "api.xf-yun.com", f"/v1/private/{server_id}"
        date = format_date_time(mktime(datetime.now().timetuple()))
        signature = f"host: {host}\ndate: {date}\nPOST {path} HTTP/1.1"
        sign = base64.b64encode(
            hmac.new(api_secret.encode(), signature.encode(), digestmod=hashlib.sha256).digest()
        ).decode()
        auth = base64.b64encode(f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{sign}"'.encode()).decode()
        return url + "?" + urlencode({"host": host, "date": date, "authorization": auth})

    data = {
        "header": {"app_id": appid, "status": 3},
        "parameter": {
            server_id: {
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
                "encoding": "jpg", "status": 3,
                "image": base64.b64encode(id_photo_bytes).decode()
            },
            "input2": {
                "encoding": "jpg", "status": 3,
                "image": base64.b64encode(live_photo_bytes).decode()
            }
        }
    }

    url = get_signed_url()
    headers = {'Content-Type': 'application/json', 'host': 'api.xf-yun.com', 'app_id': appid}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    result = json.loads(response.content.decode())

    text = base64.b64decode(result['payload']['face_compare_result']['text']).decode()
    return json.loads(text)
