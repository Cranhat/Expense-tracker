import psycopg2
<<<<<<< HEAD
from db_init import *

class Database:
    def __init__(self, host="localhost", dbname="postgres", user="postgres", password="postgres", port=5432):
=======
from backend.app.database.db_init import *

class Database:
    def __init__(self, host="localhost", dbname="postgres", user="postgres", password="postgres", port=5432):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
>>>>>>> 2ab24b4 (added basic functionality)
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
<<<<<<< HEAD
        self.cursor.execute(query)
        self.conn.commit()
=======
        if (len(query) > 0): # not empty
            self.cursor.execute(query)
            self.conn.commit()
>>>>>>> 2ab24b4 (added basic functionality)
    
    def initializeTables(self):
        self.sendQuery(users_initialization)
        self.sendQuery(accounts_initialization)
        self.sendQuery(transactions_initialization)
<<<<<<< HEAD
        self.sendQuery(categories_initialization)
        self.sendQuery(customizable_initalization)
=======
        # self.sendQuery(categories_initialization)
        # self.sendQuery(customizable_initalization)
>>>>>>> 2ab24b4 (added basic functionality)

    def fetchData(self):
        return 0
 