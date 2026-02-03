from flask import Flask
from database_persistence import DatabasePersistence

app = Flask(__name__)

storage = DatabasePersistence()
storage.test_connection()

@app.route('/')
def index():
    return "Hello World"

if __name__ == '__main__':
    app.run(port=5003)
