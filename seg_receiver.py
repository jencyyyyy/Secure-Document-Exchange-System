from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl

class SEGReceiverHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_len = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_len)
            xml_data = post_body.decode('utf-8')
            
            # Log successful mTLS connection
            client_cert = self.connection.getpeercert()
            if client_cert:
                print("[+] Successful mTLS connection established with client:")
                print(f"    Client certificate: {client_cert.get('subject')}")
            
            # Print the received XML document
            print("[+] Received XML securely:")
            print(xml_data)

            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Received securely")
            
        except ValueError as e:
            print("[x] Error decoding XML data:", e)
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Bad Request: Invalid XML data")
        except Exception as e:
            print("[x] Server Error:", e)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal Server Error")

def run_receiver():
    try:
        server_address = ('localhost', 4443)
        httpd = HTTPServer(server_address, SEGReceiverHandler)

        # Set up SSL context
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile='receiver.crt', keyfile='receiver.key')
        context.load_verify_locations(cafile='rootCA.pem')
        context.verify_mode = ssl.CERT_REQUIRED

        # Wrap socket with SSL
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

        print("[*] SEG-Receiver is listening securely on https://localhost:4443")
        httpd.serve_forever()

    except FileNotFoundError as e:
        print("[x] Error: Certificate or key file not found:", e)
    except ssl.SSLError as e:
        print("[x] SSL Configuration Error:", e)
    except Exception as e:
        print("[x] Server Startup Error:", e)

if __name__ == "__main__":
    run_receiver()
