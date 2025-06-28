from http.server import BaseHTTPRequestHandler
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle GET requests
        with app.app_context():
            response = app.test_client().get(self.path)
            self.send_response(response.status_code)
            for header, value in response.headers:
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response.data)
    
    def do_POST(self):
        # Handle POST requests
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        with app.app_context():
            response = app.test_client().post(
                self.path,
                data=post_data,
                headers=dict(self.headers)
            )
            self.send_response(response.status_code)
            for header, value in response.headers:
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response.data) 