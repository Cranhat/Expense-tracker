import psycopg2
from backend.app.database.db_init import *

class Database:
    def __init__(self, host="localhost", dbname="postgres", user="postgres", password="postgres", port=5432):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        self.conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
        self.cursor = self.conn.cursor()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if(exc_type or exc_value or exc_traceback):
            print(f"exc_type: {exc_type}, exc_value: {exc_value}, exc_traceback: {exc_traceback}")
        self.cursor.close()
        self.conn.close()
    
    def __str__(self):
        return f"host: {self.host}, dbname: {self.dbname}, user: {self.user}, password: {self.password}, port: {self.port}"
    
    def sendQuery(self, query):
        if (len(query) > 0): # not empty
            self.cursor.execute(query)
            self.conn.commit()
    
    def initializeTables(self):
        self.sendQuery(users_initialization)
        self.sendQuery(accounts_initialization)
        self.sendQuery(transactions_initialization)
        self.sendQuery(user_groups_initialization)
        self.sendQuery(group_transactions_initialization)

    def fetchData(self, query):
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data
 
    def removeData(self, query):
        try:
            self.sendQuery(query)
            self.connection.commit()
        except Exception as e:
            print(f"Error deleting task: {e}")
        