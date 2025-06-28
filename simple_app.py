from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    print("Starting simple Flask app...")
    print("Try accessing: http://127.0.0.1:3000")
    app.run(host='127.0.0.1', port=3000, debug=True) 