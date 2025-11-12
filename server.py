import http.server
import ssl
import socket
from http.server import BaseHTTPRequestHandler

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        message = f"Hello World from {socket.gethostname()}"
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(message.encode())

PORT = 443
httpd = http.server.HTTPServer(("", PORT), HelloHandler)

# SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="/cert.crt", keyfile="/cert.key")
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"HTTPS Hello World from {socket.gethostname()} on port {PORT}")
httpd.serve_forever()
