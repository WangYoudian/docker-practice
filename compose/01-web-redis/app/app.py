
import os
import redis
from http.server import HTTPServer, BaseHTTPRequestHandler

r = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=6379, decode_responses=True)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        count = r.incr("visits")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(f"Visit count: {count}\n".encode())

port = int(os.environ.get("PORT", 8000))
HTTPServer(("0.0.0.0", port), Handler).serve_forever()
