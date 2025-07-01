#!/usr/bin/env python3
"""
Deployment script for Railway
This script initializes the database and runs migrations
"""

import os
import sys
from app import create_app, db
from models import User, Question, Quiz, QuizQuestion, UserQuiz, Suggestion
from flask_migrate import upgrade

def init_db():
    """Initialize the database"""
    app = create_app('production')
    
    with app.app_context():
        # Run database migrations
        print("Running database migrations...")
        upgrade()
        
        # Create tables if they don't exist
        print("Creating database tables...")
        db.create_all()
        
        print("Database initialization complete!")

if __name__ == '__main__':
    init_db() 