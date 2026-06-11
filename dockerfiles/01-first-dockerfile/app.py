
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        name = os.environ.get("NAME", "Docker")
        self.wfile.write(f"Hello from {name}!\n".encode())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), HelloHandler)
    print(f"Serving on port {port}...")
    server.serve_forever()
