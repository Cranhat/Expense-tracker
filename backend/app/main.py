from backend.app.database.Database import *
from backend.app.database.db_init import * 
from backend.app.database.db_crud import *

def main():
    with Database() as db:
        db.initializeTables()