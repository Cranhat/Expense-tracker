import requests
import pandas as pd

def fetch_data(api):
    try:
        response = requests.get(api)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        return []
    
def get_db(df: str):
    APIS = {
        "users": "http://127.0.0.1:8000/users",
        "accounts": "http://127.0.0.1:8000/accounts",
        "transactions": "http://127.0.0.1:8000/transactions",
        "groups": "http://127.0.0.1:8000/groups",
        "user_groups": "http://127.0.0.1:8000/user_groups",
        "group_transactions": "http://127.0.0.1:8000/group_transactions",
    }

    COLUMNS = {
        "users": ["ID", "First name", "Second name", "Last name", "Username", "Email", "Created at"],
        "accounts": ["ID", "User ID", "Name", "Type", "Balance", "Created at", "Currency"],
        "transactions": ["ID", "From account ID", "To account ID", "Amount", "Currency",
                         "Category", "Description", "Transaction at", "Created at"],
        "groups": ["ID", "Name", "Owned by", "Created at"],
        "user_groups": ["User ID", "Group ID", "Role", "Joined at"],
        "group_transactions": ["ID", "Group ID", "Paid by", "Amount", "Currency", "Description", "Created at"],
    }

    if df not in APIS:
        raise ValueError(f"Unknown dataset '{df}'. Must be one of: {list(APIS.keys())}")

    data = fetch_data(APIS[df])
    result = pd.DataFrame(data, columns=COLUMNS[df])

    return result