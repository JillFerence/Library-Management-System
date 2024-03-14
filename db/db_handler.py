import sqlite3
from sqlite3 import Error

class DatabaseHandler:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = self.create_connection()

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(DatabaseHandler.__name__ + ":", e)

    def execute_query(self, query, params):
        try:
            c = self.conn.cursor()
            c.execute(query, params)
            self.conn.commit()
            return c
        except Error as e:
            print(DatabaseHandler.__name__ + ":", e)

    def fetch_one(self, query, params):
        c = self.execute_query(query, params)
        if c:
            return c.fetchone()
        else:
            return None
    
    def fetch_all(self, query, params):
        c = self.execute_query(query, params)
        if c:
            return c.fetchall()
        else:
            return []
        
    def close_connection(self):
        status = self.conn.close()
        if status:
            print("Connection closed")
        else:
            print("Connection is already closed")
