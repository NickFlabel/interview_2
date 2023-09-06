import dotenv
import os
import sqlite3

dotenv.load_dotenv()

DATABASE = os.getenv('DATABASE')

class DatabaseManager:

    class ConnectionManager:

        def __enter__(self):
            self.connection = sqlite3.connect(DATABASE)
            self.cursor = self.connection.cursor()
            return self.cursor

        def __exit__(self, *args):
            self.connection.close()

    def __init__(self, table_name: str) -> None:
        self.table_name = table_name

    def get_data(self):
        with self.ConnectionManager() as cursor:
            cursor.execute(f'SELECT * FROM {self.table_name}')
            return cursor.fetchall()
        
    def save_data(self, data):
        with self.ConnectionManager() as cursor:
            query = f'INSERT INTO {self.table_name} VALUES {data}'
            cursor.execute(query)
            cursor.connection.commit()
            return cursor.lastrowid

