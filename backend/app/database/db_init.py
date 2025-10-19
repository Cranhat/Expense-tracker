users_initialization = """
    CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY,
<<<<<<< HEAD
        name VARCHAR(255),
        second_name VARCHAR(255),
        surname VARCHAR(255),
        date_of_birth DATE,
        gender CHAR,
        account_number INT
=======
        name TEXT,
        second_name TEXT,
        surname TEXT,
        date_of_birth DATE,
        gender CHAR,
        account_number INT,
        creation_date DATE
>>>>>>> 2ab24b4 (added basic functionality)
    );
    """

accounts_initialization = """
<<<<<<< HEAD

"""

transactions_initialization = """

"""

categories_initialization = """

"""

customizable_initalization = """

"""
=======
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
>>>>>>> 2ab24b4 (added basic functionality)
