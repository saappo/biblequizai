from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    responses = db.relationship('UserResponse', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # Easy, Medium, Hard
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy=True)

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=False)  # Store options as JSON array
    correct_answer = db.Column(db.String(500), nullable=False)
    explanation = db.Column(db.Text)  # Optional explanation for the answer
    difficulty = db.Column(db.String(20), nullable=False)  # Easy, Medium, Hard
    category = db.Column(db.String(50))  # Old Testament, New Testament, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    question_hash = db.Column(db.String(64), unique=True, nullable=False)  # SHA-256 hash of question text
    
    # Relationships
    responses = db.relationship('UserResponse', backref='question', lazy=True)

    @staticmethod
    def generate_hash(text, options, correct_answer):
        """Generate a unique hash for a question based on its content"""
        import hashlib
        # Sort options to ensure same questions with different option orders are considered duplicates
        sorted_options = sorted(options)
        content = f"{text.lower().strip()}{''.join(sorted_options)}{correct_answer.lower().strip()}"
        return hashlib.sha256(content.encode()).hexdigest()

class UserResponse(db.Model):
    __tablename__ = 'user_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    response = db.Column(db.String(500), nullable=False)
    is_correct = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, user_id, question_id, response, timestamp=None):
        self.user_id = user_id
        self.question_id = question_id
        self.response = response
        self.timestamp = timestamp or datetime.utcnow()
        # Set is_correct based on the question's correct answer
        question = Question.query.get(question_id)
        if question:
            self.is_correct = (response == question.correct_answer)

class Suggestion(db.Model):
    __tablename__ = 'suggestions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContactMessage {self.id}: {self.subject}>' 