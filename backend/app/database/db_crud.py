def create_insert_user(id, name, sender_id, second_name, surname, username, email, creation_date):
    return f"""
        INSERT INTO users (id, name, sender_id, second_name, surname, username, email, creation_date)
        VALUES ({id}, {name}, {sender_id}, {second_name}, {surname}, {username}< {email}, {creation_date});
        """
    
def create_insert_account(id, user_id, name, account_type, balance, creation_date, currency):
    return f"""
        INSERT INTO accounts (id, user_id, name, account_type, balance, creation_date, currency)
        VALUES ({id}, {user_id}, {name}, {account_type}, {balance}, {creation_date}, {currency})
        """

def create_insert_transaction(id, account_id, amount, currency, category, description, created_at):
    return f"""
        INSERT INTO transactions (id, account_id, amount, currency, category, description, created_at)
        VALUES ({id}, {account_id}, {amount}, {currency}, {category}, {description}< {created_at});
        """

def create_insert_groups(id, name, owner_user_id, created_at):
    return f""" 
        INSERT INTO groups (id, name, owner_user_id, created_at)
        VALUES ({id}, {name}, {owner_user_id}, {created_at});
        """

def create_insert_user_groups(user_id, group_id, role, joined_at):
    return f""" 
        INSERT INTO user_groups (user_id, group_id, role, joined_at)
        VALUES ({user_id}, {group_id}, {role}, {joined_at});
"""

def create_insert_group_transactions(id, group_id, paid_by_user_id, amount, currency, description, created_at):
    return f""" 
        INSERT INTO group_transactions (id, group_id, paid_by_user_id, amount, currency, description, created_at)
        VALUES ({id}, {group_id}, {paid_by_user_id}, {amount}, {currency}, {description}, {created_at});
"""
