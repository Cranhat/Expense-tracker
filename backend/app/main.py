from backend.app.database.Database import *
from backend.app.database.db_init import * 

import threading

def main():
    with Database() as db:
        db.initializeTables()
        