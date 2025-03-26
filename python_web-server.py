import logging
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Define host and port
HOST = "0.0.0.0"  # Listens on all interfaces
PORT = 3000       # Port to serve on

# Set up logging
logging.basicConfig(level=logging.INFO)

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            # Customize the response here if needed
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Python Web Server</h1></body></html>")
            logging.info(f"Handled GET request from {self.client_address}")
        except Exception as e:
            self.send_error(500, str(e))
            logging.error(f"Error handling request: {e}")

if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), CustomHandler)
    logging.info(f"Serving on http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("\nShutting down server...")
        server.server_close()
    except Exception as e:
        logging.error(f"Server error: {e}")
