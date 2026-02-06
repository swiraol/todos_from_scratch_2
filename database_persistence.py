import psycopg2 
from psycopg2.extras import DictCursor 

class DatabasePersistence:
    def __init__(self):
        pass 
    def _database_connect(self):
        return psycopg2.connect("dbname=todos")
    
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

        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query)
                lists = cursor.fetchall()
        return lists
    
    def find_todos(self, list_id):
        query = """
            SELECT * FROM todos WHERE list_id = %s
        """

        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (list_id,))
                rows = cursor.fetchall()
                rows = [dict(row) for row in rows]
        return rows
    
    def find_list(self, list_id):
        query = """
            SELECT * FROM lists WHERE id = %s
        """

        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (list_id,))
                list = dict(cursor.fetchone())
        
        todos = self.find_todos(list_id)
        list['todos'] = todos 

        return list