import logging
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import socket
import time

HOST = "0.0.0.0"
PORT = 3333

TCP_STATES = {
    '01': 'ESTABLISHED',
    '02': 'SYN_SENT',
    '03': 'SYN_RECV',
    '04': 'FIN_WAIT1',
    '05': 'FIN_WAIT2',
    '06': 'TIME_WAIT',
    '07': 'CLOSE',
    '08': 'CLOSE_WAIT',
    '09': 'LAST_ACK',
    '0A': 'LISTEN',
    '0B': 'CLOSING'
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def parse_tcp_states():
    state_count = {name: 0 for name in TCP_STATES.values()}
    try:
        with open("/proc/net/tcp", "r") as f:
            lines = f.readlines()[1:]  # Skip header
            for line in lines:
                parts = line.strip().split()
                state_code = parts[3]
                state_name = TCP_STATES.get(state_code, "UNKNOWN")
                state_count[state_name] = state_count.get(state_name, 0) + 1
    except Exception as e:
        logging.error(f"Failed to parse /proc/net/tcp: {e}")
    return state_count

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/tcpstates":
            self.handle_tcpstates()
        else:
            try:
                super().do_GET()
                logging.info(f"Served GET request: {self.path} from {self.client_address}")
            except Exception as e:
                self.send_error(500, "Internal Server Error")
                logging.error(f"Error handling GET request: {e}")

    def handle_tcpstates(self):
        state_data = parse_tcp_states()
        response = {
            "timestamp": int(time.time()),
            "tcp_states": state_data
        }

        response_body = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response_body)

        logging.info(f"Returned TCP state info to {self.client_address}")

if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), CustomHandler)
    logging.info(f"Serving HTTP with TCP state endpoint at http://{HOST}:{PORT}/tcpstates")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down server...")
        server.shutdown()
        server.server_close()
    except Exception as e:
        logging.error(f"Server error: {e}")
