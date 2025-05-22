# seg_receiver.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl

class SEGReceiverHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len)
        print("[+] Received XML securely:")
        print(post_body.decode())

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Received securely")

def run_receiver():
    server_address = ('localhost', 4443)
    httpd = HTTPServer(server_address, SEGReceiverHandler)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='receiver.crt', keyfile='receiver.key')
    context.load_verify_locations(cafile='rootCA.pem')
    context.verify_mode = ssl.CERT_REQUIRED

    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print("[*] SEG-Receiver is listening securely on https://localhost:4443")
    httpd.serve_forever()

if __name__ == "__main__":
    run_receiver()
