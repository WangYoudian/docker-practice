
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        user = os.environ.get("USER", "unknown")
        self.wfile.write(f"Running as: {user} (UID: {os.getuid()})\n".encode())

HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
