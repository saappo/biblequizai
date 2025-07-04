#!/usr/bin/env python3
"""
Deployment helper script for Bible Quiz AI
Checks for common deployment issues and provides guidance
"""

import os
import sys
import importlib.util

def check_requirements():
    """Check if all required packages are available"""
    print("🔍 Checking requirements...")
    
    required_packages = [
        'flask',
        'gunicorn', 
        'flask_sqlalchemy',
        'flask_login',
        'requests',
        'python_dotenv',
        'psycopg2'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are available")
    return True

def check_environment():
    """Check environment variables"""
    print("\n🔍 Checking environment variables...")
    
    # Check for production environment
    flask_env = os.environ.get('FLASK_ENV')
    if flask_env == 'production':
        print("✅ FLASK_ENV=production")
    else:
        print(f"ℹ️  FLASK_ENV={flask_env or 'not set'}")
    
    # Check for database URL
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith('postgres'):
            print("✅ DATABASE_URL (PostgreSQL) - Found")
        else:
            print(f"ℹ️  DATABASE_URL - {database_url[:20]}...")
    else:
        print("⚠️  DATABASE_URL - Not set (will use SQLite locally)")
    
    # Check for secret key
    secret_key = os.environ.get('SECRET_KEY')
    if secret_key:
        print("✅ SECRET_KEY - Found")
    else:
        print("⚠️  SECRET_KEY - Not set (will use default)")
    
    return True

def check_files():
    """Check if required files exist"""
    print("\n🔍 Checking required files...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'render.yaml',
        'config.py',
        'models.py',
        'routes.py'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files exist")
    return True

def main():
    """Main deployment check function"""
    print("🚀 Bible Quiz AI - Deployment Check")
    print("=" * 40)
    
    checks_passed = True
    
    # Run all checks
    if not check_files():
        checks_passed = False
    
    if not check_requirements():
        checks_passed = False
    
    check_environment()
    
    print("\n" + "=" * 40)
    if checks_passed:
        print("✅ All checks passed! Your app should deploy successfully.")
        print("\n📋 Next steps:")
        print("1. Push your code to GitHub/GitLab")
        print("2. Connect your repository to Render")
        print("3. Set environment variables in Render dashboard:")
        print("   - FLASK_ENV=production")
        print("   - SECRET_KEY=<your-secret-key>")
        print("   - DATABASE_URL=<render-postgres-url>")
        print("4. Deploy!")
    else:
        print("❌ Some checks failed. Please fix the issues above before deploying.")
        sys.exit(1)

if __name__ == '__main__':
    main() 