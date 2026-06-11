
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK\n")
        elif self.path == "/slow":
            time.sleep(5)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Finally\n")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Healthy demo\n")

HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
