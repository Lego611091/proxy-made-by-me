import http.server
import socketserver
import requests

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            target_url = self.path.lstrip("/")
            print(f"Proxying: {target_url}")

            response = requests.get(target_url)

            self.send_response(response.status_code)
            self.send_header("Content-Type", response.headers.get("Content-Type", "text/html"))
            self.end_headers()

            self.wfile.write(response.content)

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Proxy error: {e}".encode())

PORT = 8080
with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    print(f"Proxy running on http://127.0.0.1:{PORT}")
    httpd.serve_forever()
