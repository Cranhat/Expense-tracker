from backend.app.database.db_init import *
from backend.app.database.db_read import *
from backend.app.database.db_create import *
from backend.app.database.db_remove import *
from backend.app.database.db_update import *
from backend.app.database.objects import *
from datetime import datetime
from fastapi import FastAPI
from fastapi import Depends
import psycopg2


class Database:
    def __init__(self, host="localhost", dbname="postgres", user="postgres", password="postgres", port=5432):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        self.app = FastAPI()
        self._setup_routes()
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if(exc_type or exc_value or exc_traceback):
            print(f"exc_type: {exc_type}, exc_value: {exc_value}, exc_traceback: {exc_traceback}")
    
    def __str__(self):
        return f"host: {self.host}, dbname: {self.dbname}, user: {self.user}, password: {self.password}, port: {self.port}"
    
    def get_conn(self):
        return psycopg2.connect(host=self.host, dbname=self.dbname, user=self.user, password=self.password, port=self.port)
    
    def sendQuery(self, query, conn, curr):
        curr.execute(query)

    def commit(self, conn, curr):
        conn.commit()

    def close_conn(self, conn, curr):
        curr.close()
        conn.close()

    def get_db(self):
        conn = self.get_conn()
        curr = conn.cursor()
        try:
            yield conn, curr
        finally:
            self.close_conn(conn, curr)
    
    def initializeTables(self):
        conn = self.get_conn()
        curr = conn.cursor()

        self.sendQuery(users_initialization, conn, curr)
        self.sendQuery(accounts_initialization, conn, curr)
        self.sendQuery(transactions_initialization, conn, curr)
        self.sendQuery(groups_initialization, conn, curr)
        self.sendQuery(user_groups_initialization, conn, curr)
        self.sendQuery(group_transactions_initialization, conn, curr)
        self.sendQuery(passwords_initialization, conn, curr)
        conn.commit()

        self.close_conn(conn, curr)

    def fetchData(self, query, conn, curr):
        curr.execute(query)
        data = curr.fetchall()
        return data
 
    def _setup_routes(self):
        @self.app.get("/")
        def read_root():
            return {"message": "Welcome!"}
        

        # --- Users --- 
        @self.app.get("/users") # get users
        def get_users(db = Depends(self.get_db)):
            conn, curr = db
            query = create_fetch().format(*('*', 'users'))
            data = self.fetchData(query, conn, curr)
            return {"data": data} 
        
        @self.app.get("/users/{id}") # get user
        def get_user(id: int, db = Depends(self.get_db)):
            conn, curr = db
            query = create_fetch_where().format(*('*', 'users', f'id = {id}'))
            data = self.fetchData(query, conn, curr)
            return {"id": id, "data": data} 
        
        @self.app.post("/users/") # post user
        async def create_user(user: User, db = Depends(self.get_db)):
            conn, curr = db
            query = create_insert_user().format(*(user.id, user.name, user.second_name, user.surname, user.username, user.email, user.creation_date))
            self.sendQuery(query, conn, curr)
            self.commit(conn, curr)
            return {"message": f"User added"}

        @self.app.put("/users/{id}") # put user
        def update_user(id: int, user: User, db = Depends(self.get_db)):
            conn, curr = db
            query = create_update_user().format(*(user.id, user.name, user.second_name, user.surname, user.username, user.email, user.creation_date)) 
            self.sendQuery(query, conn, curr)
            self.commit(conn, curr)
            return {"message": f"User updated"}

        @self.app.delete("/users/{id}") # delete user
        def delete_user(id: int, db = Depends(self.get_db)):
            conn, curr = db
            self.sendQuery(create_remove().format(*("users", f"id = {id}")), conn, curr)
            self.commit(conn, curr)
            return {"message": f"User {id} deleted"}
        

        # --- Accounts --- 

        @self.app.get("/accounts") # get account
        def get_accounts(db = Depends(self.get_db)):
            conn, curr = db
            query = create_fetch().format(*('*', 'accounts'))
            data = self.fetchData(query, conn, curr)
            return {"data": data}
        
        @self.app.get("/accounts/{id}") # get accounts
        def get_account(id: int, db = Depends(self.get_db)):
            conn, curr = db
            query = create_fetch_where().format(*('*', 'accounts', f'id = {id}'))
            data = self.fetchData(query, conn, curr)
            return {"id": id, "data": data}
        
        @self.app.get("/accounts//{id}") # get accounts
        def get_user_account(id: int, db = Depends(self.get_db)):
            conn, curr = db
            query = create_fetch_where().format(*('*', 'accounts', f'user_id = {id}'))
            data = self.fetchData(query, conn, curr)
            return {"id": id, "data": data}
        
        @self.app.post("/accounts/") # post account
        async def create_account(account: Account, db = Depends(self.get_db)):
            conn, curr = db
            query = create_insert_account().format(*(account.id, account.user_id, account.name, account.type, account.balance, account.creation_date, account.currency))
            self.sendQuery(query, conn, curr)
            self.commit(conn, curr)
            return {"message": f"Account added"}
    
        @self.app.put("/accounts/{id}") # put account
        def update_account(id: int, account: Account, db = Depends(self.get_db)):
            conn, curr = db
            query = create_update_account().format(*(account.id, account.user_id, account.name, account.type, account.balance, account.creation_date, account.currency)) 
            self.sendQuery(query, conn, curr)
            self.commit(conn, curr)
            return {"message": f"Account updated"}
        
        @self.app.delete("/accounts/{id}") # delete account
        def delete_account(id: int, db = Depends(self.get_db)):
            conn, curr = db
            self.sendQuery(create_remove().format(*("accounts", f"id = {id}")), conn, curr)
            self.commit(conn, curr)
            return {"message": f"Account {id} deleted"}


        # --- Transactions --- 
        # @self.app.get("/transactions/{id}") # get transaction
        # def get_transaction(id: int, db = Depends(self.get_db)):
        #     conn, curr = db
        #     query = create_fetch_where().format(*('*', 'transactions', f'id = {id}'))
        #     data = self.fetchData(query, conn, curr)
        #     return {"id": id, "data": data}
        
        @self.app.get("/transactions") # get transactions
        def get_transactions(db = Depends(self.get_db)):
            conn, curr = db
            query = create_fetch().format(*('*', 'transactions'))
            data = self.fetchData(query, conn, curr)
            return {"data": data}
        
        @self.app.post("/transactions/") # post transaction
        async def create_transaction(transaction: Transaction, db = Depends(self.get_db)):
            conn, curr = db
            query = create_insert_transaction().format(*(transaction.id, transaction.from_account_id, transaction.to_account_id, transaction.amount, transaction.currency, transaction.category, transaction.description, transaction.transaction_at, transaction.created_at))
            self.sendQuery(query, conn, curr)
            self.commit(conn, curr)
            return {"message": f"Transaction added"}
    
        @self.app.put("/transactions/{id}") # put transaction
        def update_transaction(id: int, transaction: Transaction, db = Depends(self.get_db)):
            conn, curr = db
            query = create_update_transaction().format(*(transaction.id, transaction.from_account_id, transaction.to_account_id, transaction.amount, transaction.currency, transaction.category, transaction.description, transaction.transaction_at, transaction.created_at)) 
            self.sendQuery(query, conn, curr)
            self.commit(conn, curr)
            return {"message": f"Transaction updated"}
        
        @self.app.delete("/transactions/{id}") # delete transaction
        def delete_transaction(id: int, db = Depends(self.get_db)):
            conn, curr = db
            self.sendQuery(create_remove().format(*("transactions", f"id = {id}")), conn, curr)
            self.commit(conn, curr)
            return {"message": f"Transaction {id} deleted"}
        

        # --- Groups --- 
        @self.app.get("/groups/{id}") # get group
        def get_group(id: int, db = Depends(self.get_db)):
            conn, curr = db
            query = create_fetch_where().format(*('*', 'groups', f'id = {id}'))
            data = self.fetchData(query, conn, curr)
            return {"id": id, "data": data}
        
        @self.app.get("/groups") # get groups
        def get_groups(db = Depends(self.get_db)):
            conn, curr = db
            query = create_fetch().format(*('*', 'groups'))
            data = self.fetchData(query, conn, curr)
            return {"data": data}
        
        @self.app.post("/groups/") # post group
        async def create_group(group: Group, db = Depends(self.get_db)):
            conn, curr = db
            query = create_insert_group().format(*(group.id, group.name, group.owner_user_id, group.created_at))
            self.sendQuery(query, conn, curr)
            self.commit(conn, curr)
            return {"message": f"Group added"}
    
        @self.app.put("/groups/{id}") # put group
        def update_group(id: int, group: Group, db = Depends(self.get_db)):
            conn, curr = db
            query = create_update_group().format(*(group.id, group.name, group.owner_user_id, group.created_at)) 
            self.sendQuery(query, conn, curr)
            self.commit(conn, curr)
            return {"message": f"Group updated"}
        
        @self.app.delete("/groups/{id}") # delete group
        def delete_group(id: int, db = Depends(self.get_db)):
            conn, curr = db
            self.sendQuery(create_remove().format(*("groups", f"id = {id}")), conn, curr)
            self.commit(conn, curr)
            return {"message": f"Group {id} deleted"}

        
        # --- User groups --- 
        @self.app.get("/user_group/{user_id}") # get user_group
        def get_user_group(user_id: int, db = Depends(self.get_db)):
            conn, curr = db
            query = create_fetch_where().format(*('*', 'user_groups', f'user_id = {user_id}'))
            data = self.fetchData(query, conn, curr)
            return {"id": user_id, "data": data}
        
        @self.app.get("/user_groups") # get user_groups
        def get_user_groups(db = Depends(self.get_db)):
            conn, curr = db
            query = create_fetch().format(*('*', 'user_groups'))
            data = self.fetchData(query, conn, curr)
            return {"data": data}
        
        @self.app.post("/user_groups/") # post user_group
        async def create_user_group(user_group: User_Group, db = Depends(self.get_db)):
            conn, curr = db
            query = create_insert_user_group().format(*(user_group.user_id, user_group. group_id, user_group.role, user_group.joined_at))
            self.sendQuery(query, conn, curr)
            self.commit(conn, curr)
            return {"message": f"Group added"}
    
        @self.app.put("/user_groups/{id}") # put user_group
        def update_user_group(id: int, user_group: User_Group, db = Depends(self.get_db)):
            conn, curr = db
            query = create_update_user_group().format(*(user_group.user_id, user_group. group_id, user_group.role, user_group.joined_at)) 
            self.sendQuery(query, conn, curr)
            self.commit(conn, curr)
            return {"message": f"User group updated"}
        
        @self.app.delete("/user_groups/{id}") # delete user_group
        def delete_user_group(id: int, db = Depends(self.get_db)):
            conn, curr = db
            self.sendQuery(create_remove().format(*("user_groups", f"group_id = {id}")), conn, curr)
            self.commit(conn, curr)
            return {"message": f"User group {id} deleted"}
        
        @self.app.delete("/user_groups/{group_id}/{user_id}") # delete member
        def delete_member(group_id: int, user_id: int, db = Depends(self.get_db)):
            conn, curr = db
            self.sendQuery(create_remove_member().format(*("user_groups", f"group_id = {group_id}", f"user_id = {user_id}")), conn, curr)
            self.commit(conn, curr)
            return {"message": f"User group {id} deleted"}

        
        # --- Group transactions --- 
        @self.app.get("/group_transactions/{id}") # get group_transaction
        def get_group_transaction(id: int, db = Depends(self.get_db)):
            conn, curr = db
            query = create_fetch_where().format(*('*', 'group_transactions', f'group_id = {id}'))
            data = self.fetchData(query, conn, curr)
            return {"id": id, "data": data}
        
        @self.app.get("/group_transactions") # get group_transactions
        def get_group_transactions(db = Depends(self.get_db)):
            conn, curr = db
            query = create_fetch().format(*('*', 'group_transactions'))
            data = self.fetchData(query, conn, curr)
            return {"data": data}
        
        @self.app.post("/group_transactions/") # post group_transaction
        async def create_group_transaction(group_transaction: GroupTransaction, db = Depends(self.get_db)):
            conn, curr = db
            query = create_insert_group_transaction().format(*(group_transaction.id, group_transaction.group_id, group_transaction.paid_by_user_id, group_transaction.amount, group_transaction.currency, group_transaction.description, group_transaction.created_at))
            self.sendQuery(query, conn, curr)
            self.commit(conn, curr)
            return {"message": f"Group Transaction added"}
    
        @self.app.put("/group_transactions/{id}") # put group_transaction
        def update_group_transaction(id: int, group_transaction: GroupTransaction, db = Depends(self.get_db)):
            conn, curr = db
            query = create_update_group_transaction().format(*(group_transaction.id, group_transaction.group_id, group_transaction.paid_by_user_id, group_transaction.amount, group_transaction.currency, group_transaction.description, group_transaction.created_at)) 
            self.sendQuery(query, conn, curr)
            self.commit(conn, curr)
            return {"message": f"Group Transaction updated"}
        
        @self.app.delete("/group_transactions/{id}") # delete group_transaction
        def delete_group_transaction(id: int, db = Depends(self.get_db)):
            conn, curr = db
            self.sendQuery(create_remove().format(*("group_transactions", f"id = {id}")), conn, curr)
            self.commit(conn, curr)
            return {"message": f"Group Transaction {id} deleted"}
        

        # --- Passwords --- 
        @self.app.get("/passwords/{user_id}") # get password
        def get_password(user_id: int, db = Depends(self.get_db)):
            conn, curr = db
            query = create_fetch_where().format(*('*', 'passwords', f'user_id = {user_id}'))
            data = self.fetchData(query, conn, curr)
            return {"user_id": user_id, "data": data}
        
        @self.app.post("/passwords/") # post password
        async def create_password(password: Password, db = Depends(self.get_db)):
            conn, curr = db
            query = create_insert_password().format(*(password.user_id, password.password))
            self.sendQuery(query, conn, curr)
            self.commit(conn, curr)
            return {"message": f"password created"}
    
        @self.app.put("/passwords/{user_id}") # put password
        def update_password(id: int, password: Password, db = Depends(self.get_db)):
            conn, curr = db
            query = create_update_passowrd().format(*(password.user_id, password.password)) 
            self.sendQuery(query, conn, curr)
            self.commit(conn, curr)
            return {"message": f"password updated"}
        
        @self.app.delete("/passwords/{user_id}") # delete password
        def delete_password(user_id: int, db = Depends(self.get_db)):
            conn, curr = db
            self.sendQuery(create_remove().format(*("passwords", f"user_id = {user_id}")), conn, curr)
            self.commit(conn, curr)
            return {"message": f"password {user_id} deleted"}
        
        #################################################### nicole

        @self.app.get("/users/{id}/groups")
        def get_this_user_groups(id: int, db = Depends(self.get_db)):
            conn, curr = db

            query = f"""
                SELECT 
                    ug.group_id AS group_id,
                    ug.user_id AS user_id,
                    g.name AS group_name,
                    uo.username AS owner_username,
                    ug.role AS role,
                    ug.joined_at AS joined_at
                FROM user_groups ug
                LEFT JOIN groups g ON ug.group_id = g.id
                LEFT JOIN users uo ON g.owner_user_id = uo.id
                WHERE ug.user_id = {id}
                ORDER BY ug.joined_at;
            """

            data = self.fetchData(query, conn, curr)

            return {"user_id": id, "groups": data}
        


        @self.app.get("/groups/{group_id}/data")
        def get_this_group(group_id: int, db = Depends(self.get_db)):
            conn, curr = db

            query = f"""
                SELECT 
                    ug.user_id AS user_id,
                    u.username AS username,
                    uo.username AS owner_username,
                    g.owner_user_id AS owner_id,
                    ug.role AS role,
                    ug.joined_at AS joined_at,
                    g.name AS group_name
                FROM user_groups ug
                LEFT JOIN users u ON ug.user_id = u.id
                LEFT JOIN groups g ON ug.group_id = g.id
                LEFT JOIN users uo ON g.owner_user_id = uo.id
                WHERE ug.group_id = {group_id}
                ORDER BY ug.joined_at;
            """
            data = self.fetchData(query, conn, curr)

            return {"data": data}
        

        @self.app.get("/transactions/{id}")
        def display_transactions(id: int, db = Depends(self.get_db)):
            conn, curr = db

            query = f"""
                SELECT *
                FROM transactions
                WHERE
                    (from_account_id = {id} AND amount < 0)
                OR
                    (to_account_id  = {id} AND amount > 0) 
                ORDER BY created_at;
            """
            data = self.fetchData(query, conn, curr)
            return {"data": data}
        