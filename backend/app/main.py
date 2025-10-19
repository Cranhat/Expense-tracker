from backend.app.database.Database import *
from backend.app.database.db_init import * 

def main():
    with Database() as db:
<<<<<<< HEAD
        db.sendQuery(users_initialization)
        db.initialize_tables()
=======
        db.initializeTables()
>>>>>>> 2ab24b4 (added basic functionality)
        