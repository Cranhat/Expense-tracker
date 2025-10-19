from backend.app.database.Database import *
from backend.app.database.db_init import * 

def main():
    with Database() as db:
        db.sendQuery(users_initialization)
        db.initialize_tables()
        