import requests
import pandas as pd

def fetch_data(api):
    try:
        response = requests.get(api)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        return []

def get_db():
    USERS_API = "http://127.0.0.1:8000/users"
    ACCOUNTS_API = "http://127.0.0.1:8000/accounts"
    TRANSACTIONS_API = "http://127.0.0.1:8000/transactions"
    GROUPS_API = "http://127.0.0.1:8000/groups"
    USER_GROUPS_API = "http://127.0.0.1:8000/user_groups"
    GROUP_TANSACTIONS_API = "http://127.0.0.1:8000/group_transactions"

    users_list = fetch_data(USERS_API)
    accounts_list = fetch_data(ACCOUNTS_API)
    transactions_list = fetch_data(TRANSACTIONS_API)
    groups_list = fetch_data(GROUPS_API)
    user_groups_list = fetch_data(USER_GROUPS_API)
    group_transactions_list = fetch_data(GROUP_TANSACTIONS_API)

    user_columns = ["ID", "First name", "Second name", "Last name", "Username", "Email", "Created at"]
    accounts_columns = ["ID", "User ID", "Name", "Type", "Balance", "Created at", "Currency"]
    transactions_columns = ["ID", "From account ID", "Account ID", "Amount", "Currency", "Category", "Description", "Transaction at", "Created at"]
    groups_columns = ["ID", "Name", "Owned by", "Created at"]
    user_groups_columns = ["User ID", "Group ID", "Role", "Joined at"]
    group_transactions_colums = ["ID", "Paid by", "Amount", "Currency", "Description", "Created at"]

    df_users = pd.DataFrame(users_list, columns=user_columns)
    df_accounts = pd.DataFrame(accounts_list, columns=accounts_columns)
    df_transactions = pd.DataFrame(transactions_list, columns=transactions_columns)
    df_groups = pd.DataFrame(groups_list, columns=groups_columns)
    df_user_groups = pd.DataFrame(user_groups_list, columns=user_groups_columns)
    df_group_transactions = pd.DataFrame(group_transactions_list, columns=group_transactions_colums)

    return df_users, df_accounts, df_transactions, df_groups, df_user_groups, df_group_transactions