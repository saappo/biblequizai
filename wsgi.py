import os
from app import create_app

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'your-secure-secret-key-here'  # Change this to a secure key

# Create the application instance
application = create_app('production')

if __name__ == '__main__':
    application.run() 