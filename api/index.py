from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Bible Quiz AI</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .container { max-width: 600px; margin: 0 auto; }
                .button { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 10px; display: inline-block; }
                .button:hover { background: #0056b3; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎯 Bible Quiz AI</h1>
                <p>Welcome to your Bible Quiz application!</p>
                <p>✅ Railway deployment is working successfully!</p>
                
                <h2>Choose your difficulty:</h2>
                <a href="/api/quiz/Easy" class="button">Easy Quiz</a>
                <a href="/api/quiz/Medium" class="button">Medium Quiz</a>
                <a href="/api/quiz/Hard" class="button">Hard Quiz</a>
                
                <h3>Test Endpoints:</h3>
                <a href="/api/test" class="button">Test API</a>
                <a href="/api/health" class="button">Health Check</a>
            </div>
        </body>
        </html>
        """
        
        self.wfile.write(html_content.encode())
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "message": "POST request received",
            "status": "success"
        }
        
        self.wfile.write(json.dumps(response).encode()) 