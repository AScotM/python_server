import logging
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

# Define host and port
HOST = "0.0.0.0"  # Listens on all interfaces
PORT = 3000       # Port to serve on

# Set up logging with a more readable format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests."""
        try:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Python Web Server</h1></body></html>")
            logging.info(f"Handled GET request from {self.client_address}")
        except Exception as e:
            self.send_error(500, "Internal Server Error")
            logging.error(f"Error handling GET request: {e}")

    def do_POST(self):
        """Handle POST requests (example for JSON handling)."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8")

            try:
                data = json.loads(post_data)  # Parse JSON
                response = {"status": "success", "received": data}
                response_body = json.dumps(response).encode("utf-8")

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(response_body)

                logging.info(f"Handled POST request from {self.client_address} - Data: {data}")
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
                logging.warning(f"Invalid JSON received from {self.client_address}")

        except Exception as e:
            self.send_error(500, "Internal Server Error")
            logging.error(f"Error handling POST request: {e}")

if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), CustomHandler)
    logging.info(f"Serving on http://{HOST}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("\nShutting down server...")
        server.shutdown()  # Gracefully shut down the server
        server.server_close()
    except Exception as e:
        logging.error(f"Server error: {e}")
