#!/usr/bin/env python3
"""
WSGI entry point for Railway deployment
"""

import os
from app import create_app

# Create the Flask app
app = create_app('production')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 