from backend.app.database.Database import *
from backend.app.database.db_init import * 
from backend.app.database.db_create import *

import uvicorn

db = Database()
db.initializeTables()
app = db.app

def main():
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)


        