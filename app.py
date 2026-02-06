from flask import (
            Flask, 
            g, 
            redirect,
            render_template, 
            url_for,   
) 
from database_persistence import DatabasePersistence 

app = Flask(__name__)

@app.before_request 
def db_storage():
    g.storage = DatabasePersistence()

@app.route("/")
def index():
    return redirect(url_for('all_lists'))

@app.route("/lists")
def all_lists():
    lists = g.storage.all_lists()
    return render_template('lists.html', all_lists=lists)

@app.route("/lists/<int:list_id>")
def show_list(list_id):
    lst = g.storage.find_list(list_id)
    return render_template('list.html', lst=lst)

if __name__ == "__main__":
    app.run(debug=True, port=5003)