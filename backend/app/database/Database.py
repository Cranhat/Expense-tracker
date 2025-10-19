import psycopg2
from db_init import *

class Database:
    def __init__(self, host="localhost", dbname="postgres", user="postgres", password="postgres", port=5432):
        self.conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
        self.cursor = self.conn.cursor()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.cursor.close()
        self.conn.close()
    
    def __str__(self):
        return f"host: {self.host}, dbname: {self.dbname}, user: {self.user}, password: {self.password}, port: {self.port}"
    
    def sendQuery(self, query):
        self.cursor.execute(query)
        self.conn.commit()
    
    def initializeTables(self):
        self.sendQuery(users_initialization)
        self.sendQuery(accounts_initialization)
        self.sendQuery(transactions_initialization)
        self.sendQuery(categories_initialization)
        self.sendQuery(customizable_initalization)

    def fetchData(self):
        return 0
 