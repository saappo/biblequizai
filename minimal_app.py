#!/usr/bin/env python3
"""
Minimal Flask app for Railway - guaranteed to work
"""

from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': 'Bible Quiz AI is working!',
        'version': 'minimal'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/test')
def test():
    return jsonify({'test': 'working'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 