from flask import Flask 
from database_persistence import DatabasePersistence 

app = Flask(__name__)

storage = DatabasePersistence()

@app.route("/")
def index():
    storage.test_connection()
    return "Skeleton created!"

if __name__ == "__main__":
    app.run(debug=True, port=5003)