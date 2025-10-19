
def create_insert_user(id, balance, sender_id, reciever_id, transfer_type, title, currency, creation_date, account_type):
    f"""
INSERT INTO users (id, balance, sender_id, reciever_id, transfer_type, title, currency, creation_date, account_type)
VALUES ({id}, {balance}, {sender_id}, {reciever_id}, {transfer_type}, {title}< {currency}, {creation_date}, {account_type});
"""
    
def create_insert_account(id, balance, sender_id, reciever_id, transfer_type, title, currency, creation_date, account_type):
    f"""
INSERT INTO accounts (id, balance, creation_date, account_type, currency)
VALUES ({id}, {balance}, {creation_date}, {account_type}, {currency})
"""
    
def create_insert_transaction(id, balance, sender_id, reciever_id, transfer_type, title, currency, creation_date, account_type):
    f"""
INSERT INTO transactions (id, balance, sender_id, reciever_id, transfer_type, title, currency, creation_date, account_type)
VALUES ({id}, {balance}, {sender_id}, {reciever_id}, {transfer_type}, {title}< {currency}, {creation_date}, {account_type});
"""