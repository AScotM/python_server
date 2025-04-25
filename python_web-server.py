import logging
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HOST = "0.0.0.0"
PORT = 3333

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        """Serve directory contents or files."""
        try:
            super().do_GET()  # Use built-in logic
            logging.info(f"Served GET request: {self.path} from {self.client_address}")
        except Exception as e:
            self.send_error(500, "Internal Server Error")
            logging.error(f"Error handling GET request: {e}")

    def do_POST(self):
        """Handle POST requests with JSON payload."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8")

            try:
                data = json.loads(post_data)
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
    logging.info(f"Serving directory content on http://{HOST}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down server...")
        server.shutdown()
        server.server_close()
    except Exception as e:
        logging.error(f"Server error: {e}")
