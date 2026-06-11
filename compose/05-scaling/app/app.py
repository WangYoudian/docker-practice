
import os
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        hostname = socket.gethostname()
        self.wfile.write(f"Served by: {hostname}\n".encode())

port = int(os.environ.get("PORT", 5000))
HTTPServer(("0.0.0.0", port), Handler).serve_forever()
