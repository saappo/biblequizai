#!/usr/bin/env python3
"""
Secure Database Setup Script
This script helps you set up your database securely for development.
"""

import os
import secrets
from app import create_app
from models import db, User

def generate_secret_key():
    """Generate a secure random secret key"""
    return secrets.token_hex(32)

def setup_database():
    """Initialize the database with secure defaults"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Check if admin user exists
        admin_email = "admin@biblequizai.com"
        admin = User.query.filter_by(email=admin_email).first()
        
        if not admin:
            # Create admin user
            admin = User(email=admin_email, is_guest=False)
            admin.set_password("admin123")  # Change this in production!
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created!")
            print(f"   Email: {admin_email}")
            print(f"   Password: admin123")
            print("   ⚠️  Remember to change this password!")
        else:
            print("✅ Admin user already exists")

def main():
    print("🔒 BibleQuizAI Secure Setup")
    print("=" * 40)
    
    # Generate a secure secret key
    secret_key = generate_secret_key()
    print(f"🔑 Generated Secret Key: {secret_key}")
    print()
    
    # Setup database
    print("📊 Setting up database...")
    setup_database()
    print()
    
    # Security recommendations
    print("🛡️  Security Recommendations:")
    print("1. Create a .env file with your secret key")
    print("2. Never commit .env file to git")
    print("3. Use strong passwords in production")
    print("4. Regularly backup your database")
    print("5. Monitor for suspicious activity")
    print()
    
    print("✅ Setup complete! Your app is ready to run securely.")

if __name__ == "__main__":
    main() 