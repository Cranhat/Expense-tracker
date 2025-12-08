def create_insert_user():
    return """
    INSERT INTO users (id, name, second_name, surname, username, email, creation_date)
    VALUES ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');
    """
    
def create_insert_account():
    return """
    INSERT INTO accounts (id, user_id, name, type, balance, creation_date, currency)
    VALUES ({0}, {1}, '{2}', '{3}', {4}, '{5}' , '{6}')
    """
    
def create_insert_transaction():
    return """
    INSERT INTO transactions (id, from_account_id, to_account_id, amount, currency, category, description, transaction_at, created_at)
    VALUES ({0}, {1}, {2}, {3}, '{4}', '{5}', '{6}', '{7}', '{8}');
    """

def create_insert_group():
    return """
    INSERT INTO groups (id, name, owner_user_id, created_at)
    VALUES ({0}, '{1}', {2}, '{3}');
    """

def create_insert_user_group():
    return  """
    INSERT INTO user_groups (user_id, group_id, role, joined_at)
    VALUES ({0}, {1}, '{2}', '{3}');
    """

def create_insert_group_transaction():
    return """
    INSERT INTO group_transactions (id, group_id, paid_by_user_id, amount, currency, description, created_at)
    VALUES ({0}, {1}, {2}, {3}, '{4}', '{5}', '{6}');
    """

def create_insert_password():
    return """
    INSERT INTO passwords (user_id, password)
    VALUES ({0}, '{1}');
    """
