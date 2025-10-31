users_initialization = """
    CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY,
        name TEXT,
        second_name TEXT,
        surname TEXT,
        username TEXT,
        email TEXT,
        creation_date DATE
    );
    """

accounts_initialization = """
    CREATE TABLE IF NOT EXISTS accounts (
        id INT PRIMARY KEY,
        user_id INT,
        name TEXT,
        type int,
        balance FLOAT,
        creation_date DATE,
        currency TEXT
    );
    """

transactions_initialization = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INT PRIMARY KEY,
        account_id INT,
        amount INT,
        currency TEXT,
        category TEXT,
        description TEXT,
        transaction_at DATE,
        created_at DATE
    );
    """

groups_initialization = """
    CREATE TABLE IF NOT EXISTS groups (
        id INT PRIMARY KEY,
        name TEXT,
        owner_user_id INT,
        created_at DATE
); """

user_groups_initialization = """
    CREATE TABLE IF NOT EXISTS user_groups (
        user_id INT,
        group_id INT,
        role TEXT,
        joined_at DATE
); """

group_transactions_initialization = """
    CREATE TABLE IF NOT EXISTS group_transactions (
        id INT PRIMARY KEY,
        group_id INT,
        paid_by_user_id INT,
        amount INT,
        currency TEXT,
        description TEXT,
        created_at DATE
); """
