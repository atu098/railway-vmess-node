#!/usr/bin/env python3
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

UUID = os.environ.get("UUID", "")
SUB_TOKEN = os.environ.get("SUB_TOKEN", "")

with open("/app/surge.tmpl", encoding="utf-8") as f:
    SURGE_TMPL = f.read()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        u = urlparse(self.path)
        if u.path.rstrip("/") == "/sub/surge.conf":
            qs = parse_qs(u.query)
            if SUB_TOKEN and qs.get("token", [""])[0] != SUB_TOKEN:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"forbidden")
                return
            uuid = UUID or "UUID-NOT-SET"
            host = self.headers.get("Host", "").split(":")[0]
            domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN") or host or "YOUR-DOMAIN.up.railway.app"
            body = SURGE_TMPL.replace("${DOMAIN}", domain).replace("${UUID}", uuid)
            data = body.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        elif u.path.rstrip("/") == "/sub":
            host = self.headers.get("Host", "")
            token_qs = f"?token={SUB_TOKEN}" if SUB_TOKEN else ""
            msg = f"订阅链接: https://{host}/sub/surge.conf{token_qs}\n"
            data = msg.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 10001), Handler).serve_forever()
