import streamlit as st
import requests
import pandas as pd

#python3 -m streamlit run webapp.py

USERS_API = "http://127.0.0.1:8000/users"
TRANSACTIONS_API = "http://127.0.0.1:8000/transactions"
ACCOUNTS_API = "http://127.0.0.1:8000/accounts"
GROUPS_API = "http://127.0.0.1:8000/groups"
USER_GROUPS_API = "http://127.0.0.1:8000/user_groups"
GROUP_TANSACTIONS_API = "http://127.0.0.1:8000/group_transactions"


st.title("Expense Tracker")
# --- users ---
try:
    users_response = requests.get(USERS_API)
    users_response.raise_for_status()
    users = users_response.json()
    users_list = users.get("data", [])
except Exception as e:
    st.error(f"Error fetching users: {e}")
    users = []

# --- transactions ---
try:
    transactions_response = requests.get(TRANSACTIONS_API)
    transactions_response.raise_for_status()
    transactions = transactions_response.json()
    transactions_list = transactions.get("data", [])
except Exception as e:
    st.error(f"Error fetching transactions: {e}")
    users = []

# --- accounts ---
try:
    accounts_response = requests.get(ACCOUNTS_API)
    accounts_response.raise_for_status()
    accounts = accounts_response.json()
    accounts_list = accounts.get("data", [])
except Exception as e:
    st.error(f"Error fetching accounts: {e}")
    users = []

# --- groups ---
try:
    groups_response = requests.get(GROUPS_API)
    groups_response.raise_for_status()
    groups = groups_response.json()
    groups_list = groups.get("data", [])
except Exception as e:
    st.error(f"Error fetching groups: {e}")
    users = []
    

# --- user_groups ---
try:
    user_groups_response = requests.get(USER_GROUPS_API)
    user_groups_response.raise_for_status()
    user_groups = user_groups_response.json()
    user_groups_list = user_groups.get("data", [])
except Exception as e:
    st.error(f"Error fetching user_groups: {e}")
    users = []

# --- group_transactions ---
try:
    group_transactions_response = requests.get(GROUP_TANSACTIONS_API)
    group_transactions_response.raise_for_status()
    group_transactions = group_transactions_response.json()
    group_transactions_list = group_transactions.get("data", [])
except Exception as e:
    st.error(f"Error fetching group_accounts {e}")
    users = []


st.subheader("Users")
columns = ["id", "First name", "Second name", "Last name", "Username", "Email", "Created At"]
df_users = pd.DataFrame(users_list, columns=columns)
df_users = df_users.reset_index(drop=True)
st.table(df_users.style.hide(axis="index"))

st.subheader("Transactions")
df_transactions = pd.DataFrame(transactions_list)
st.table(df_transactions)

st.subheader("Accounts")
df_accounts = pd.DataFrame(accounts_list)
st.table(df_accounts)

st.subheader("Groups")
df_groups = pd.DataFrame(groups_list)
st.table(df_groups)

st.subheader("User groups")
df_user_groups = pd.DataFrame(user_groups_list)
st.table(df_user_groups)

st.subheader("Group transactions")
df_group_transactions = pd.DataFrame(group_transactions_list)
st.table(df_group_transactions)

st.title("Create User")

id = st.text_input("id")
name = st.text_input("name")
second_name = st.text_input("second_name")
surname = st.text_input("surname")
username = st.text_input("username")
email = st.text_input("email")
creation_date = st.text_input("creation_date")

if st.button("Submit"):
    data = {
        "id" : id,
        "name": name,
        "second_name": second_name,
        "surname": surname,
        "username": username,
        "email": email,
        "creation_date": creation_date,
    }

    response = requests.post("http://127.0.0.1:8000/users/", json=data)

    if response.status_code == 200:
        st.success("User created successfully!")
        st.json(response.json())
    else:
        st.error("Failed to create user")
        st.write(response.text)

st.title("Update User")

id = st.text_input("id")
name = st.text_input("name")
second_name = st.text_input("second_name")
surname = st.text_input("surname")
username = st.text_input("username")
email = st.text_input("email")
creation_date = st.text_input("creation_date")

# if st.button("Update User Submit"):
#     data = {
#         "id" : id,
#         "name": name,
#         "second_name": second_name,
#         "surname": surname,
#         "username": username,
#         "email": email,
#         "creation_date": creation_date,
#     }

#     response = requests.put(f"http://127.0.0.1:8000/users/{id}", json=data)

#     if response.status_code == 200:
#         st.success("User updated successfully!")
#         st.json(response.json())
#     else:
#         st.error("Failed to update user")
#         st.write(response.text)



# del_id = st.text_input("del_id")
# if st.button("Delete"):
#     response = requests.delete(f"http://127.0.0.1:8000/users/{del_id}")
#     if response.status_code == 200:
#         st.success("User deleted successfully!")
#         st.json(response.json())
#     else:
#         st.error("Failed to delete user")
#         st.write(response.text)