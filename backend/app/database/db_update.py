def create_update_user():
    return """
    UPDATE users 
    SET 
    id = {0},
    name = '{1}',
    second_name = '{2}',
    surname = '{3}',
    username = '{4}',
    email = '{5}',
    creation_date = '{6}'
    WHERE id = {0}
    """

def create_update_account():
    return """
    UPDATE accounts 
    SET 
    id = {0},
    user_id = {1},
    name = '{2}',
    type = '{3}',
    balance = {4},
    creation_date = '{5}',
    currency = '{6}'
    WHERE id = {0}
    """

def create_update_transaction():
    return """
    UPDATE transactions 
    SET 
    id = {0},
    from_account_id = {1},
    to_account_id = {2},
    amount = {3},
    currency = '{4}',
    category = '{5}',
    description = '{6}',
    transaction_at = '{7}',
    created_at = '{8}'
    WHERE id = {0}
    """

def create_update_group():
    return """
    UPDATE groups 
    SET 
    id = {0},
    name = '{1}',
    owner_user_id = {2},
    created_at = '{3}'
    WHERE id = {0}
    """

def create_update_user_group():
    return """
    UPDATE user_groups 
    SET 
    user_id = {0},
    group_id = {1},
    role = '{2}',
    joined_at = '{3}'
    WHERE id = {0}
    """

def create_update_group_transaction():
    return """
    UPDATE group_transactions 
    SET 
    id = {0},
    group_id = {1},
    paid_by_user_id = {2},
    amount = {3},
    currency = '{4}',
    description = '{5}',
    created_at = '{6}'
    WHERE id = {0}
    """