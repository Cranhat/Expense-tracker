
def create_insert_user():
    return """
    INSERT INTO users (id, name, second_name, surname, email, creation_date)
    VALUES ({0}, {1}, {2}, {3}, {4}, {5});
    """
    
def create_insert_account(id, balance, sender_id, reciever_id, transfer_type, title, currency, creation_date, account_type):
    return """
    INSERT INTO accounts (id, balance, creation_date, account_type, currency)
    VALUES ({0}, {1}, {2}, {3}, {4})
    """
    
def create_insert_transaction(id, balance, sender_id, reciever_id, transfer_type, title, currency, creation_date, account_type):
    return """
    INSERT INTO transactions (id, balance, sender_id, reciever_id, transfer_type, title, currency, creation_date, account_type)
    VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8});
    """