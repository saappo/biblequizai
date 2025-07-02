import os
from flask import Flask, jsonify

# Create a simple Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-please-change'

# Root route
@app.route('/')
def home():
    return jsonify({
        'message': 'Bible Quiz AI is running!',
        'status': 'success',
        'version': 'minimal-working'
    })

# Health check route for Railway
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Bible Quiz AI is running!'
    })

# Test route
@app.route('/test')
def test():
    return jsonify({
        'status': 'working',
        'message': 'Test endpoint is working!'
    })

# Explicitly export the app for gunicorn
application = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 