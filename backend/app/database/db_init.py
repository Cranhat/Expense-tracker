users_initialization = """
    CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY,
        name TEXT,
        second_name TEXT,
        surname TEXT,
        date_of_birth DATE,
        gender CHAR,
        account_number INT,
        creation_date DATE
    );
    """

accounts_initialization = """
    CREATE TABLE IF NOT EXISTS account (
        id INT PRIMARY KEY,
        balance FLOAT,
        creation_date DATE,
        account_type INT,
        currency TEXT
    );
    """

transactions_initialization = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INT PRIMARY KEY,
        balance FLOAT,
        sender_id INT,
        reciever_id INT,
        transfer_type INT,
        title TEXT,
        currency TEXT,
        creation_date DATE,
        account_type INT
    );
    """

# categories_initialization = """

# """

# customizable_initalization = """

# """
