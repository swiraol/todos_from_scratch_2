import psycopg2 

class DatabasePersistence:
    def __init__(self):
        pass

    def _database_connect(self):
        connection = psycopg2.connect(
            dbname="todos_from_scratch_2",
            
        )
        return connection 
    def test_connection(self):
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                print("✅ Database Connection Successful!")
        

