from backend.app.database.db_init import *
from backend.app.database.db_read import *
from backend.app.database.db_create import *
from backend.app.database.db_remove import *
from backend.app.database.db_update import *
from backend.app.database.objects import *

from datetime import datetime
from fastapi import FastAPI
import psycopg2

class Database:
    def __init__(self, host="localhost", dbname="postgres", user="postgres", password="postgres", port=5432):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        self.conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
        self.cursor = self.conn.cursor()
        self.app = FastAPI()
        self._setup_routes()
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if(exc_type or exc_value or exc_traceback):
            print(f"exc_type: {exc_type}, exc_value: {exc_value}, exc_traceback: {exc_traceback}")
        self.cursor.close()
        self.conn.close()
    
    def __str__(self):
        return f"host: {self.host}, dbname: {self.dbname}, user: {self.user}, password: {self.password}, port: {self.port}"
    
    def _setup_routes(self):

        @self.app.get("/")
        def read_root():
            return {"message": "Welcome!"}
        
        # --- Users --- 
        @self.app.get("/users/{id}")
        def get_user(id: int):
            query = create_fetch_where().format(*('*', 'users', f'id = {id}'))
            data = self.fetchData(query)
            return {"id": id, "data": data} 
        
        @self.app.post("/users/")
        async def create_user(user: User):
            self.sendQuery(create_insert_user().format(*(
                user.id,
                user.name,
                user.second_name,
                user.surname,
                user.username,
                user.email,
                user.creation_date)))
            return {
                    "message": "we got data succesfully",
                    "user_id": user.id,
                    "username": user.username,
                    }
        
        @self.app.put("/users/") # <---
        def update_user(id: int, user: User):
            query = create_update().format(*(user))
            return {"message": f"User {id} updated", "user": user}

        @self.app.delete("/users/{id}")
        def delete_user(id: int, user: User):
            self.sendQuery(create_remove().format(*("users:", f"id = {id}")))
            return {"message": f"User {id} deleted"}
        
        # --- Accounts --- 
        @self.app.get("/accounts/{id}")
        def get_account(id: int):
            query = create_fetch_where().format(*('*', 'accounts', f'id = {id}'))
            data = self.fetchData(query)
            return {"id": id, "data": data}
    
        # --- Transactions --- 
        @self.app.get("/transactions/{id}")
        def get_transaction(id: int):
            query = create_fetch_where().format(*('*', 'transactions', f'id = {id}'))
            data = self.fetchData(query)
            return {"id": id, "data": data}
        
        # --- Groups --- 
        @self.app.get("/groups/{id}")
        def get_group(id: int):
            query = create_fetch_where().format(*('*', 'groups', f'id = {id}'))
            data = self.fetchData(query)
            return {"id": id, "data": data}
        
        # --- User groups --- 
        @self.app.get("/user_group/{user_id}")
        def get_user_group(user_id: int):
            query = create_fetch_where().format(*('*', 'user_groups', f'user_id = {user_id}'))
            data = self.fetchData(query)
            return {"id": user_id, "data": data}
        
        # --- Group transactions --- 
        @self.app.get("/group_transactions/{id}")
        def get_group_transaction(id: int):
            query = create_fetch_where().format(*('*', 'group_transactions', f'id = {id}'))
            data = self.fetchData(query)
            return {"id": id, "data": data}
        
        
    def sendQuery(self, query):
        if (query):
            self.cursor.execute(query)
            self.conn.commit()
            return 1
        return 0

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
            self.conn.commit()
        except Exception as e:
            print(f"Error deleting task: {e}")
    

        