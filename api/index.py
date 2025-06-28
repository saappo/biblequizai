from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-please-change')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///biblequiz.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Simple models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    choices = db.Column(db.Text, nullable=False)  # JSON string
    correct_index = db.Column(db.Integer, nullable=False)
    verse = db.Column(db.String(200))
    difficulty = db.Column(db.String(20), default='Easy')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/public-quiz/<difficulty>', methods=['GET', 'POST'])
def public_quiz(difficulty):
    if request.method == 'GET':
        # Get questions for the difficulty level
        questions = Question.query.filter_by(difficulty=difficulty).limit(5).all()
        
        if not questions:
            # Create sample questions if none exist
            sample_questions = {
                'Easy': [
                    {
                        'question': 'Who built the ark?',
                        'choices': ['Noah', 'Moses', 'Abraham', 'David'],
                        'correct_index': 0,
                        'verse': 'Genesis 6:9'
                    }
                ],
                'Medium': [
                    {
                        'question': 'How many disciples did Jesus have?',
                        'choices': ['10', '12', '13', '14'],
                        'correct_index': 1,
                        'verse': 'Matthew 10:1'
                    }
                ],
                'Hard': [
                    {
                        'question': 'What was the name of the mountain where Moses received the Ten Commandments?',
                        'choices': ['Mount Sinai', 'Mount Horeb', 'Mount Ararat', 'Mount Moriah'],
                        'correct_index': 0,
                        'verse': 'Exodus 19:20'
                    }
                ]
            }
            
            # Add sample questions to database
            for q_data in sample_questions.get(difficulty, []):
                question = Question(
                    question=q_data['question'],
                    choices=json.dumps(q_data['choices']),
                    correct_index=q_data['correct_index'],
                    verse=q_data['verse'],
                    difficulty=difficulty
                )
                db.session.add(question)
            
            db.session.commit()
            questions = Question.query.filter_by(difficulty=difficulty).limit(5).all()
        
        # Format questions for template
        quiz_questions = []
        for q in questions:
            quiz_questions.append({
                'question': q.question,
                'choices': json.loads(q.choices),
                'correct_index': q.correct_index,
                'verse': q.verse
            })
        
        return render_template('quiz.html', questions=quiz_questions, difficulty=difficulty)
    
    else:  # POST request
        # Handle quiz submission
        score = 0
        total_questions = 0
        
        for key, value in request.form.items():
            if key.startswith('answer_'):
                question_id = int(key.split('_')[1])
                question = Question.query.get(question_id)
                if question and int(value) == question.correct_index:
                    score += 1
                total_questions += 1
        
        percentage = (score / total_questions * 100) if total_questions > 0 else 0
        
        return render_template('results.html', 
                             score=score, 
                             total=total_questions, 
                             percentage=percentage)

# Vercel serverless function handler
def handler(request, context):
    """Handler for Vercel serverless functions"""
    with app.app_context():
        return app(request, context)

# Create tables
with app.app_context():
    db.create_all() 