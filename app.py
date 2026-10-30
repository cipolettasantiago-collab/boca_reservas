"""Boca Reservas — servicio de prueba de Telegram (sin reservas)."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlencode
from urllib.request import Request, urlopen

def send_test():
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    payload = urlencode({"chat_id":chat_id,"text":"🟦🟨 BOCA RESERVAS — PRUEBA\nEsta es una notificación de prueba. NO hay ninguna entrada reservada."}).encode()
    with urlopen(Request(f"https://api.telegram.org/bot{token}/sendMessage",data=payload),timeout=12) as res:
        return json.load(res).get("ok",False)

class Handler(BaseHTTPRequestHandler):
    def reply(self,code,obj):
        b=json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",str(len(b)))
        self.end_headers()
        self.wfile.write(b)
    def do_GET(self):
        if self.path=="/health":
            return self.reply(200,{"status":"ok","telegram_configured":all(os.getenv(k) for k in ("TELEGRAM_BOT_TOKEN","TELEGRAM_CHAT_ID")),"monitor_active":False,"reservation_active":False})
        self.reply(404,{"error":"not found"})
    def do_POST(self):
        if self.path!="/test-telegram":return self.reply(404,{"error":"not found"})
        if not os.getenv("ADMIN_TEST_KEY") or self.headers.get("X-Admin-Key")!=os.getenv("ADMIN_TEST_KEY"):
            return self.reply(403,{"error":"unauthorized"})
        try:
            return self.reply(200 if send_test() else 502,{"sent":True,"type":"simulation","reservation":False})
        except Exception:
            self.reply(503,{"sent":False,"error":"Telegram not configured or delivery failed"})
if __name__=="__main__":
    try:
        print("TELEGRAM_TEST_SENT", send_test(), flush=True)
    except Exception as exc:
        print("TELEGRAM_TEST_FAILED", type(exc).__name__, flush=True)
    ThreadingHTTPServer(("0.0.0.0",int(os.getenv("PORT","10000"))),Handler).serve_forever()
