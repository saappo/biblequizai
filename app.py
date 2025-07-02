import os
from flask import Flask, jsonify, render_template, request, redirect, url_for
from datetime import datetime

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-please-change-in-production')

# Root route with improved HTML response
@app.route('/')
def home():
    return render_template('index.html')

# Health check route for Render
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Bible Quiz AI is running on Render!',
        'timestamp': datetime.utcnow().isoformat(),
        'environment': os.environ.get('RENDER_ENVIRONMENT', 'development')
    })

# Test route
@app.route('/test')
def test():
    return jsonify({
        'status': 'working',
        'message': 'Test endpoint is working on Render!',
        'timestamp': datetime.utcnow().isoformat()
    })

# API routes
@app.route('/api/quiz/<difficulty>')
def quiz_api(difficulty):
    return jsonify({
        'difficulty': difficulty,
        'message': f'Quiz API endpoint for {difficulty} difficulty',
        'status': 'success'
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found',
        'status': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'Something went wrong on our end',
        'status': 500
    }), 500

# Explicitly export the app for gunicorn
application = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug) 