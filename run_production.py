import os
from app import create_app

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_APP'] = 'app.py'

# Create the application instance
app = create_app('production')

if __name__ == '__main__':
    # This is just for testing the production configuration
    # In actual production, use gunicorn instead
    app.run(host='0.0.0.0', port=8000) 