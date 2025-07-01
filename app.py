import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
from config import config
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask_migrate import Migrate
from question_generator import generate_daily_questions
import atexit

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configure logging for Railway (no file handler in production)
if os.getenv('FLASK_ENV') != 'production':
    # Create a rotating file handler for development
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.DEBUG)
    
    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(handler)
else:
    # In production, just use console logging
    logging.basicConfig(level=logging.INFO)

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
scheduler = BackgroundScheduler()

# Global variable to track if scheduler is running
scheduler_running = False

def create_app(config_name='default'):
    """Create and configure the Flask application"""
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
    
    # Initialize scheduler (only in development)
    global scheduler_running
    if os.getenv('FLASK_ENV') != 'production' and not scheduler_running:
        try:
            def init_scheduler():
                try:
                    scheduler.add_job(
                        func=lambda: generate_daily_questions(),
                        trigger=CronTrigger(hour=1, minute=0),
                        id='generate_daily_questions',
                        name='Generate daily Bible quiz questions',
                        replace_existing=True
                    )
                    scheduler.start()
                    logger.info("Scheduler started successfully")
                    global scheduler_running
                    scheduler_running = True
                except Exception as e:
                    logger.error(f"Error starting scheduler: {str(e)}")
            
            with app.app_context():
                init_scheduler()
        except Exception as e:
            logger.error(f"Error initializing scheduler: {str(e)}")
    else:
        # In production, we'll use Railway's cron jobs instead
        logger.info("Running in production mode - scheduler disabled")
    
    # Register routes
    from routes import register_routes
    register_routes(app)
    
    return app

# Create the application instance
try:
    app = create_app()
    logger.info("Flask app created successfully")
except Exception as e:
    logger.error(f"Error creating Flask app: {str(e)}")
    # Create a minimal app for error handling
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fallback-key'
    
    @app.route('/')
    def fallback():
        return {'error': 'App initialization failed', 'message': str(e)}, 500

# Cleanup scheduler when app shuts down
@atexit.register
def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()

# Railway production handler
def handler(request, context):
    """Handler for Railway production"""
    with app.app_context():
        return app(request, context)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 