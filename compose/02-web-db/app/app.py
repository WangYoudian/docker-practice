
import os, time
import psycopg2
from http.server import HTTPServer, BaseHTTPRequestMaker

def get_db():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "secret"),
        dbname=os.environ.get("DB_NAME", "appdb"),
    )

class Handler(BaseHTTPRequestMaker):
    def do_GET(self):
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT count, now() FROM visits ORDER BY id DESC LIMIT 1")
            row = cur.fetchone()
            if row:
                msg = f"Visit #{row[0]} at {row[1]}\n"
            else:
                cur.execute("INSERT INTO visits (count) VALUES (1)")
                conn.commit()
                msg = "First visit!\n"
            cur.close()
            conn.close()
        except Exception as e:
            msg = f"DB error: {e}\n"

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(msg.encode())

port = int(os.environ.get("PORT", 8000))
s = HTTPServer(("0.0.0.0", port), Handler)
print(f"Listening on :{port}")
s.serve_forever()
