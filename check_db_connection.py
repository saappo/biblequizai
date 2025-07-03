#!/usr/bin/env python3
"""
Database Connection Checker
This script checks if the database is properly connected and configured.
"""

import os
from app import create_app
from models import db, User, Question, ContactMessage

def check_database_connection():
    """Check database connection and configuration"""
    print("🔍 Database Connection Checker")
    print("=" * 40)
    
    # Create app context
    app = create_app()
    
    with app.app_context():
        try:
            # Check database URI
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            print(f"📊 Database URI: {db_uri}")
            
            # Check if it's SQLite or PostgreSQL
            if 'sqlite' in db_uri:
                print("🗄️  Database Type: SQLite (Local Development)")
            elif 'postgres' in db_uri:
                print("🗄️  Database Type: PostgreSQL (Production)")
            else:
                print("❓ Database Type: Unknown")
            
            # Test connection
            print("\n🔌 Testing database connection...")
            with db.engine.connect() as conn:
                result = conn.execute(db.text("SELECT 1"))
                print("✅ Database connection successful!")
            
            # Check if tables exist
            print("\n📋 Checking database tables...")
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            expected_tables = ['users', 'quizzes', 'questions', 'user_responses', 'suggestions', 'contact_messages']
            
            for table in expected_tables:
                if table in tables:
                    print(f"✅ Table '{table}' exists")
                else:
                    print(f"❌ Table '{table}' missing")
            
            # Check if tables have data
            print("\n📊 Checking table data...")
            try:
                user_count = User.query.count()
                print(f"👥 Users: {user_count}")
            except Exception as e:
                print(f"❌ Error checking users: {e}")
            
            try:
                question_count = Question.query.count()
                print(f"❓ Questions: {question_count}")
            except Exception as e:
                print(f"❌ Error checking questions: {e}")
            
            try:
                contact_count = ContactMessage.query.count()
                print(f"📧 Contact Messages: {contact_count}")
            except Exception as e:
                print(f"❌ Error checking contact messages: {e}")
            
            # Check environment variables
            print("\n🔧 Environment Variables:")
            secret_key = os.environ.get('SECRET_KEY', 'Not set')
            flask_env = os.environ.get('FLASK_ENV', 'Not set')
            database_url = os.environ.get('DATABASE_URL', 'Not set')
            
            print(f"🔑 SECRET_KEY: {'Set' if secret_key != 'Not set' else 'Not set'}")
            print(f"🌍 FLASK_ENV: {flask_env}")
            print(f"🗄️  DATABASE_URL: {'Set' if database_url != 'Not set' else 'Not set'}")
            
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            print("\n🔧 Troubleshooting tips:")
            print("1. Check if database file exists (for SQLite)")
            print("2. Check environment variables")
            print("3. Run 'python init_db.py' to create tables")
            return False
    
    print("\n✅ Database check completed!")
    return True

if __name__ == "__main__":
    check_database_connection() 