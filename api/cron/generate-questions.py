from http.server import BaseHTTPRequestHandler
import os
import sys
import json
from datetime import datetime

# Add the parent directory to the path so we can import our app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app import create_app, db
from models import Question
from question_generator import generate_questions

def generate_daily_questions():
    """Generate daily Bible quiz questions"""
    app = create_app()
    
    with app.app_context():
        try:
            # Generate questions for each difficulty level
            for difficulty in ["Easy", "Medium", "Hard"]:
                questions = generate_questions(difficulty)
                print(f"Generated {len(questions)} {difficulty} questions")
                
        except Exception as e:
            print(f"Error generating questions: {e}")
            return False
    
    return True

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            success = generate_daily_questions()
            
            if success:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "status": "success",
                    "message": "Daily questions generated successfully",
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "status": "error",
                    "message": "Failed to generate daily questions",
                    "timestamp": datetime.utcnow().isoformat()
                }
                
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
            self.wfile.write(json.dumps(error_response).encode()) 