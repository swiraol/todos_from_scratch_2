import psycopg2 
from psycopg2.extras import DictCursor 

from werkzeug.exceptions import NotFound

class DatabasePersistence:
    def __init__(self):
        pass

    def init_db(self):
        query = """
            CREATE TABLE IF NOT EXISTS lists (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT False,
                list_id INTEGER NOT NULL REFERENCES lists (id) ON DELETE CASCADE
            );
        """

        with self._database_connect('postgres') as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'todos';")
                row = cursor.fetchone()

        if row is None:
            with self._database_connect('postgres') as conn:
                conn.autocommit = True
                with conn.cursor() as cursor:
                    cursor.execute("CREATE DATABASE todos")

        with self._database_connect('todos') as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)               

    def _database_connect(self, db_name='todos'):
        return psycopg2.connect(f"dbname={db_name}")
    
    def _query_db(self, query, parameters=None, result_type=None):
        with self._database_connect('todos') as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, parameters)
                if result_type == 'one':
                    row = cursor.fetchone()
                    return row
                elif result_type == 'all':
                    rows = cursor.fetchall()
                    return rows
                else:
                    return
    
    def all_lists(self):
        query = """
            SELECT
                l.id, 
                l.title,
                COUNT(t.id) AS total_todos,
                COUNT(CASE WHEN NOT t.completed THEN 1 END) as todos_remaining
            FROM lists l 
            LEFT JOIN todos t
            ON l.id = t.list_id
            GROUP BY l.id
            ORDER BY todos_remaining DESC, l.title
        """

        lists = self._query_db(query, result_type='all')
        return lists
    
    def find_todos(self, list_id):
        query = """
            SELECT * FROM todos WHERE list_id = %s
            ORDER BY todos.completed
        """
        rows = self._query_db(query, parameters=(list_id,), result_type='all')
        rows = [dict(row) for row in rows]
        return rows
    
    def find_todo(self, list_id, todo_id):
        query = "SELECT * FROM todos WHERE id = %s and list_id = %s"

        todo = self._query_db(query, (todo_id, list_id), 'one')
        if not todo:
            raise NotFound("Todo not found")
        
        return dict(todo)
    
    def find_list(self, list_id):
        query = """
            SELECT * FROM lists WHERE id = %s
        """

        lst = self._query_db(query, parameters=(list_id,), result_type='one')
        if lst:
            lst = dict(lst)
            todos = self.find_todos(list_id)
            lst['todos'] = todos 
            return lst
        
        return None
    
    def create_list(self, title):
        query = "INSERT INTO lists (title) VALUES (%s)"
        self._query_db(query, parameters=(title,))
    
    def create_todo(self, list_id, title):
        query = "INSERT INTO todos (title, list_id) VALUES (%s, %s)"
        self.find_list(list_id)
        self._query_db(query, (title, list_id,))

    def update_todo(self, list_id, todo_id, status):
        query = "UPDATE todos SET completed = %s WHERE list_id = %s and id = %s"
        self.find_list(list_id)
        self.find_todo(list_id, todo_id)
        self._query_db(query, parameters=(status, list_id, todo_id))

    def complete_all(self, list_id):
        query = "UPDATE todos SET completed = True WHERE list_id = %s"
        self.find_list(list_id)
        self._query_db(query, parameters=(list_id,))
    
    def update_list(self, list_id, new_title):
        query = "UPDATE lists SET title = %s WHERE id = %s"
        self.find_list(list_id)
        self._query_db(query, parameters=(new_title, list_id,))
    
    def delete_list(self, list_id):
        query = "DELETE FROM lists WHERE id = %s"
        self.find_list(list_id)
        self._query_db(query, parameters=(list_id,))
    
    def delete_todo(self, list_id, todo_id):
        query = "DELETE FROM todos WHERE id = %s and list_id = %s"
        self.find_list(list_id)
        self.find_todo(list_id, todo_id)
        self._query_db(query, parameters=(todo_id, list_id))
    