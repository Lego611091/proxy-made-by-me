import http.server
import socketserver
import requests

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Remove the leading slash
        target_url = self.path.lstrip("/")

        # Auto-fix common malformed URLs like "https:/site.com"
        if target_url.startswith("http:/") and not target_url.startswith("http://"):
            target_url = target_url.replace("http:/", "http://", 1)

        if target_url.startswith("https:/") and not target_url.startswith("https://"):
            target_url = target_url.replace("https:/", "https://", 1)

        # If no URL was supplied, show a friendly message
        if not target_url or "://" not in target_url:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(
                b"Proxy needs a valid URL after the slash, like /https://example.com"
            )
            return

        print(f"Proxying: {target_url}")

        try:
            # Forward the request to the real website
            response = requests.get(target_url)

            # Send response headers
            self.send_response(response.status_code)
            self.send_header(
                "Content-Type",
                response.headers.get("Content-Type", "text/html")
            )
            self.end_headers()

            # Send response body
            self.wfile.write(response.content)

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Proxy error: {e}".encode())

PORT = 8080
with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    print(f"Proxy running on http://127.0.0.1:{PORT}")
    httpd.serve_forever()
