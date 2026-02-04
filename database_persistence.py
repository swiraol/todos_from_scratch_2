import psycopg2 

class DatabasePersistence:
    def __init__(self):
        pass 
    def _database_connect(self):
        return psycopg2.connect("dbname=todos")

    def test_connection(self):
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM lists")
                print(f"Database connection succesful!")