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
    # redirect to /lists (import redirect and url_for)
    return redirect(url_for('all_lists'))

@app.route("/lists")
def all_lists():
    # call the db method for fetching all lists and assign to all_lists (import g object to store the data)
    all_lists = g.storage.all_lists()
    print(f"all_lists: {all_lists}")
        # db method will return the list title, list id, total todos and remaining todos counts
    # pass all_lists to lists.html for rendering
    return render_template('lists.html', all_lists=all_lists)
        # template will iterate over all_lists to display list title and fancy counts

if __name__ == "__main__":
    app.run(debug=True, port=5003)