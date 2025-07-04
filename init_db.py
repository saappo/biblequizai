#!/usr/bin/env python3
"""
Database initialization script for Bible Quiz AI
Run this on Render to set up the database tables
"""

import os
import sys
from app import create_app
from models import db, User, Question, Quiz, UserResponse, Suggestion, ContactMessage

def init_database():
    """Initialize the database with tables"""
    print("🚀 Initializing Bible Quiz AI Database...")
    
    # Create the Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            print("📋 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check if we have any questions
            question_count = Question.query.count()
            print(f"📊 Found {question_count} questions in database")
            
            # Check if we have any users
            user_count = User.query.count()
            print(f"👥 Found {user_count} users in database")
            
            print("\n🎉 Database initialization complete!")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing database: {str(e)}")
            return False

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1) 