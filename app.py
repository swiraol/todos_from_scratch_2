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
from todos.utils import error_for_title, is_list_completed
from werkzeug.exceptions import NotFound
from functools import wraps

app = Flask(__name__)

app.secret_key = "Hello"

@app.template_filter('pluralize')
def pluralize(num):
    num = int(num)
    if num == 0:
        return "No todos"
    elif num == 1:
        return f"{num} total todo"
    else:
        return f"{num} total todos"

@app.before_request 
def db_storage():
    g.storage = DatabasePersistence()

def require_list(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        list_id = kwargs.get('list_id')
        lst = g.storage.find_list(list_id)
        if not lst:
            raise NotFound("List not found")
        return f(lst, *args, **kwargs)
    return decorated_func

def require_todo(f):
    @require_list
    @wraps(f)
    def decorated_func(lst, *args, **kwargs):
        todo_id = kwargs.get('todo_id')
        list_id = kwargs.get('list_id')
        todo = g.storage.find_todo(list_id, todo_id)
        if not todo:
            raise NotFound("Todo not found")
        return f(lst, todo, *args, **kwargs)

    return decorated_func

@app.context_processor
def list_utilities_processor():
    return dict(is_list_completed=is_list_completed)

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
    
    g.storage.create_list(title)
    flash("You created a new list", "success")
    return redirect(url_for('all_lists'))

@app.route("/lists/new")
def new_list():
    return render_template('new_list.html')

@app.route("/lists/<int:list_id>")
@require_list
def show_list(lst, list_id):
    all_completed = lst['todos'] and all(t['completed'] for t in lst['todos'])
    return render_template('list.html', lst=lst, all_completed=all_completed)

@app.route("/lists/<int:list_id>/todos", methods=["POST"])
@require_list 
def create_todo(lst, list_id):
    title = request.form['todo_title']
    error = error_for_title(title)
    if error:
        flash(error, "error")
        return render_template('list.html', lst=lst, title=title)
    
    g.storage.create_todo(list_id, title)
    flash("Your todo item has been created", "success")
    return redirect(url_for("show_list", list_id=list_id))

@app.route("/lists/<int:list_id>/todos/<int:todo_id>", methods=["POST"])
@require_todo
def update_todo(lst, todo, list_id, todo_id):
    is_completed = 'true' == (request.form['completed'].lower())
    g.storage.update_todo(list_id, todo_id, is_completed)
    flash("The todo has been updated", "success")
    return redirect(url_for('show_list', list_id=list_id))

@app.route("/lists/<int:list_id>/complete_all", methods=["POST"])
@require_list 
def complete_all(lst, list_id):
    g.storage.complete_all(list_id)
    flash("All todos have been completed", "success")
    return redirect(url_for('show_list', list_id=list_id))

@app.route("/lists/<int:list_id>/edit")
@require_list 
def edit_list(lst, list_id):
    return render_template('edit_list.html', list_id=list_id, lst=lst)

@app.route("/lists/<int:list_id>", methods=["POST"])
@require_list 
def update_list(lst, list_id):
    # FIX APPLIED: Fetch all_lists for validation
    all_lists = g.storage.all_lists()
    new_title = request.form['new_title']
    
    # FIX APPLIED: Pass 'list' (lowercase) and lists=all_lists
    error = error_for_title(new_title, title_type='list', lists=all_lists)
    if error:
        flash(error, "error")
        return render_template('edit_list.html', list_id=list_id, lst=lst,  title=new_title)
    
    g.storage.update_list(list_id, new_title)
    flash("The list title has been updated", "success")

    return redirect(url_for('show_list', list_id=list_id))

@app.route("/lists/<int:list_id>/delete", methods=["POST"])
@require_list 
def delete_list(lst, list_id):
    g.storage.delete_list(list_id)
    flash("The list has been deleted", "success")
    return redirect(url_for('all_lists'))

@app.route("/lists/<int:list_id>/todos/<int:todo_id>/delete", methods=["POST"])
@require_todo
def delete_todo(lst, todo, list_id, todo_id):
    g.storage.delete_todo(list_id, todo_id)
    flash("The todo has been deleted", "success")
    return redirect(url_for('show_list', list_id=list_id))

if __name__ == "__main__":
    persistence = DatabasePersistence()
    persistence.init_db()
    app.run(debug=True, port=5003)