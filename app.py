import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db, User
from routes import register_routes
from config import Config, ProductionConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config_class=None):
    try:
        app = Flask(__name__)
        
        # Use production config on Render, development config locally
        if os.environ.get('FLASK_ENV') == 'production':
            logger.info("Using production configuration")
            app.config.from_object(ProductionConfig)
        else:
            logger.info("Using development configuration")
            app.config.from_object(Config)
        
        logger.info(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')[:50]}...")
        
        # Initialize extensions
        db.init_app(app)
        
        # Initialize Flask-Login
        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = 'login'
        login_manager.login_message = 'Please log in to access this page.'
        
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
        
        # Register routes
        register_routes(app)
        
        # Create database tables
        with app.app_context():
            logger.info("Creating database tables...")
            db.create_all()
            logger.info("Database tables created successfully")
        
        logger.info("Flask app created successfully")
        return app
        
    except Exception as e:
        logger.error(f"Error creating Flask app: {str(e)}")
        raise

# Create the application instance
try:
    app = create_app()
    logger.info("Application instance created successfully")
except Exception as e:
    logger.error(f"Failed to create application: {str(e)}")
    raise

# Explicitly export the app for gunicorn
application = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    logger.info(f"Starting app on port {port}, debug={debug}")
    app.run(host='0.0.0.0', port=port, debug=debug) 