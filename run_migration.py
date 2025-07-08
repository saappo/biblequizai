#!/usr/bin/env python3
"""
Script to run database migration for adding day and question_type columns.
"""

import os
import sys
from app import create_app
from models import db, Question, User
from sqlalchemy import text

def run_migration():
    """Run the database migration"""
    app = create_app()
    
    with app.app_context():
        try:
            print("Starting database migration...")
            
            # Check if the day column already exists
            try:
                db.session.execute(text('SELECT day FROM questions LIMIT 1'))
                print("Day column already exists, skipping migration.")
                return
            except Exception:
                pass
            
            print("Adding day and question_type columns...")
            db.session.execute(text('ALTER TABLE questions ADD COLUMN day INTEGER'))
            db.session.execute(text('ALTER TABLE questions ADD COLUMN question_type VARCHAR(50)'))
            
            try:
                db.session.execute(text('ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT FALSE'))
                print("Added is_admin column to users table.")
            except Exception as e:
                print(f"is_admin column might already exist: {e}")
            
            print("Setting default values for existing questions...")
            db.session.execute(text("UPDATE questions SET day = 1, question_type = 'Factual' WHERE day IS NULL"))
            
            print("Making columns non-nullable...")
            try:
                db.session.execute(text('ALTER TABLE questions ALTER COLUMN day SET NOT NULL'))
                db.session.execute(text('ALTER TABLE questions ALTER COLUMN question_type SET NOT NULL'))
            except Exception as e:
                print(f"Could not set NOT NULL (SQLite may not support this): {e}")
            
            try:
                db.session.execute(text('ALTER TABLE questions DROP COLUMN quiz_id'))
                print("Removed quiz_id column.")
            except Exception:
                print("quiz_id column doesn't exist or already removed.")
            
            try:
                db.session.execute(text('DROP TABLE quizzes'))
                print("Dropped quizzes table.")
            except Exception:
                print("quizzes table doesn't exist or already dropped.")
            
            db.session.commit()
            print("Migration completed successfully!")
            
            question_count = Question.query.count()
            print(f"Total questions in database: {question_count}")
            sample_questions = Question.query.limit(3).all()
            print("\nSample questions after migration:")
            for q in sample_questions:
                print(f"  Day {q.day}: {q.text[:50]}... (Type: {q.question_type})")
            
        except Exception as e:
            db.session.rollback()
            print(f"Migration failed: {str(e)}")
            raise

def create_admin_user():
    """Create an admin user if none exists"""
    app = create_app()
    
    with app.app_context():
        try:
            admin_user = User.query.filter_by(is_admin=True).first()
            if admin_user:
                print(f"Admin user already exists: {admin_user.email}")
                return
            admin_email = "admin@biblequiz.com"
            admin_password = "admin123"  # Change this in production!
            admin_user = User(
                email=admin_email,
                is_admin=True
            )
            admin_user.set_password(admin_password)
            db.session.add(admin_user)
            db.session.commit()
            print(f"Created admin user: {admin_email}")
            print(f"Password: {admin_password}")
            print("IMPORTANT: Change this password in production!")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating admin user: {str(e)}")

def main():
    print("Bible Quiz Database Migration Tool")
    print("=" * 40)
    run_migration()
    print("\n" + "=" * 40)
    create_admin_user()
    print("\nMigration and setup completed!")
    print("You can now:")
    print("1. Use the admin interface at /admin/login")
    print("2. Add questions using the add_questions.py script")
    print("3. Take quizzes with the new day-based system")

if __name__ == "__main__":
    main() 