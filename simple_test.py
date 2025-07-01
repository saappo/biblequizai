#!/usr/bin/env python3
"""
Simple test Flask app for Railway debugging
"""

from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': 'Simple Flask app is working!',
        'environment': os.getenv('FLASK_ENV', 'not set'),
        'port': os.getenv('PORT', 'not set')
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/test')
def test():
    return jsonify({'test': 'This is a test endpoint'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 