from flask import (
            flash,
            Flask, 
            g, 
            redirect,
            render_template, 
            request,
            url_for,   
) 
from todos.database_persistence import DatabasePersistence 
from todos.utils import error_for_title

app = Flask(__name__)

app.secret_key = "Hello"

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

@app.route("/lists", methods=["POST"])
def create_list():
    all_lists = g.storage.all_lists()
    title = request.form['list_title']
    error = error_for_title(title, 'list', all_lists)
    if error:
        flash(error, "error")
        return render_template('new_list.html', title=title)

    if any(title == lst['title'] for lst in all_lists):
        flash("The list title already exists")
        return render_template('new_list.html', title=title)
    
    g.storage.create_list(title)
    flash("You created a new list", "success")
    return redirect(url_for('all_lists'))

@app.route("/lists/new")
def new_list():
    return render_template('new_list.html')

@app.route("/lists/<int:list_id>")
def show_list(list_id):
    lst = g.storage.find_list(list_id)
    return render_template('list.html', lst=lst)

@app.route("/lists/<int:list_id>/todos", methods=["POST"])
def create_todo(list_id):
    todo_title = request.form['todo_title']
    error = error_for_title(todo_title)
    if error:
        flash(error, "error")
        return redirect(url_for('show_list', list_id=list_id))
    
    g.storage.create_todo(list_id, todo_title)
    flash("Your todo item has been created", "success")
    return redirect(url_for("show_list", list_id=list_id))

if __name__ == "__main__":
    app.run(debug=True, port=5003)