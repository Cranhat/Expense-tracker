
def create_insert_user():
    return """
    INSERT INTO users (id, name, second_name, surname, username, email, creation_date)
    VALUES ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');
    """
    
def create_insert_account():
    return """
    INSERT INTO accounts (id, balance, creation_date, account_type, currency)
    VALUES ({0}, {1}, '{2}', {3}, '{4}')
    """
    
def create_insert_transaction():
    return """
    INSERT INTO transactions (id, from_account_id, to_account_id, amount, currency, category, description, transaction_at, created_at, type)
    VALUES ({0}, {1}, {2}, {3}, {4}, '{5}', '{6}', '{7}', {8}, '{9}');
    """
