from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Enables CORS for all domains on all routes
# Read more: https://github.com/corydolphin/flask-cors?tab=readme-ov-file#simple-usage
CORS(app)

@app.get('/api/hello')
def hello():
    return {
        "message": "Hello from Flask"
    }

if __name__ == '__main__':
    app.run(debug=True)