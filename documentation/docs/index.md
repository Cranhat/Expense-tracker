# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout
    documentation/
        mkdocs.yml    # The configuration file.
        docs/
            index.md  # The documentation homepage.
            ...       # Other markdown  pages, images and other files.
    backend/
        app/
            database/
                conflict_resolving.py
                Database.py # Main databaseclass file
                db_create.py 
                db_init.py
                db_read.py
                db_remove.py
                db_update.py
                objects.py
    frontend/

## Postgre sql commands
Start server:
    sudo service postgresql start

Close server:
    sudo service postgresql stop

Set password:
    sudo passwd postgres

To connect with postgresql shell:
    sudo -u postgres psql

To restart postgresql service:
    sudo systemctl restart postgresql

## Uvicorn commands
uvicorn backend.app.main:app --host=127.0.0.1 --port=8000 


## Database structure
tables:

    - users
        id INT PRIMARY KEY,
        name TEXT,
        second_name TEXT,
        surname TEXT,
        username TEXT,
        email TEXT,
        creation_date DATE

    - accounts
        id INT PRIMARY KEY,
        user_id INT,
        name TEXT,
        type int,
        balance FLOAT,
        creation_date DATE,
        currency TEXT

    - transactions
        id INT PRIMARY KEY,
        from_account_id INT,
        to_account_id INT,
        amount FLOATniewiem,
        currency TEXT,
        category TEXT,
        description TEXT,
        transaction_at DATE,
        created_at DATE

    - groups
        id INT PRIMARY KEY,
        name TEXT,
        owner_user_id INT,
        created_at DATE

    - user_groups
        user_id INT,
        group_id INT,
        role TEXT,
        joined_at DATE

    - group_transactions
        id INT PRIMARY KEY,
        group_id INT,
        paid_by_user_id INT,
        amount INT,
        currency TEXT,
        description TEXT,
        created_at DATE

## HTTP request explanation
GET:
Used to read data from server.

POST:
Upload data to the server

PATCH:
Updates data on the server based on entry that already exists

DELETE:
Used to delete the data from database

## Queries overview


## Diagram of technologies cooperation


## Python program driagram