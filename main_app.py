#!/usr/bin/env python3
"""
Railway-optimized Bible Quiz AI main application
"""

import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
from config import config
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
from flask_migrate import Migrate

# Load environment variables
load_dotenv()

# Configure logging for Railway (console only)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name='production'):
    """Create and configure the Flask application for Railway"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-please-change')
    
    # Handle Railway PostgreSQL URL conversion
    database_url = os.getenv('DATABASE_URL', 'sqlite:///biblequiz.db')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    # Register routes
    from routes import register_routes
    register_routes(app)
    
    # Add a simple health check route
    @app.route('/health')
    def health_check():
        """Simple health check endpoint for Railway"""
        return {'status': 'healthy', 'message': 'Bible Quiz AI main app is running!'}
    
    return app

# Create the application instance
try:
    app = create_app()
    logger.info("Main Flask app created successfully")
    
    # Add a test route to verify the app works
    @app.route('/test-main')
    def test_main():
        return {'status': 'main app working', 'message': 'Bible Quiz AI main app is running!'}
        
except Exception as e:
    logger.error(f"Error creating main Flask app: {str(e)}")
    # Create a minimal app for error handling
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fallback-key'
    
    @app.route('/')
    def fallback():
        return {'error': 'Main app initialization failed', 'message': str(e)}, 500
    
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'error': str(e)}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 