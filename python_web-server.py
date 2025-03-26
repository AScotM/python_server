from http.server import SimpleHTTPRequestHandler, HTTPServer

# Define host and port
HOST = "0.0.0.0"  # Listens on all interfaces
PORT = 3000       # Port to serve on

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Customize the response here if needed
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Python Web Server</h1></body></html>")

if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), CustomHandler)
    print(f"Serving on http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()

