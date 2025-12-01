import streamlit as st
import requests
import pandas as pd

USERS_API = "http://127.0.0.1:8000/users"
ACCOUNTS_API = "http://127.0.0.1:8000/accounts"
TRANSACTIONS_API = "http://127.0.0.1:8000/transactions"
GROUPS_API = "http://127.0.0.1:8000/groups"
USER_GROUPS_API = "http://127.0.0.1:8000/user_groups"
GROUP_TANSACTIONS_API = "http://127.0.0.1:8000/group_transactions"

st.title("Personal Expense Tracker")

def fetch_data(api):
    try:
        response = requests.get(api)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        st.error(f"Error fetching data from {api}: {e}")
        return []

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

username_input = st.text_input("Enter your username:")
username_input = username_input.strip().lower()

if username_input:
    df_user = df_users[df_users["Username"].str.lower() == username_input]

    if df_user.empty:
        st.warning("Username not found :(")
    else:
        user_id = df_user.iloc[0]["ID"]
        first_name = df_user.iloc[0]["First name"]
        st.subheader(f"Welcome, {first_name}!")

        # acoounts
        user_accounts_df = df_accounts[df_accounts["User ID"] == user_id]
        display_user_accounts_df = user_accounts_df.drop(columns=["ID", "User ID"])
        st.subheader("Your Accounts")
        if not user_accounts_df.empty:
            st.table(display_user_accounts_df) #accounts table
            account_to_show = None

            with st.expander("Show Transactions"):
                for idx, row in user_accounts_df.iterrows():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"{row['Name']} - Balance: {row['Balance']}")
                    with col2:
                        if st.button("Load Transactions", key=f"txn_{row['ID']}"):
                            account_to_show = row['ID']

            if account_to_show is not None:
                st.subheader("Transactions")
                show_transactions = df_transactions[df_transactions["Account ID"] == account_to_show]
                show_transactions = show_transactions.drop(columns=["ID", "From account ID", "Account ID"])
                st.dataframe(show_transactions, use_container_width=True) #transactions table
        else:
            st.info("No transactions for this account.")

        # groups
        user_group_ids = df_user_groups[df_user_groups["User ID"] == user_id]["Group ID"].tolist()
        user_groups_df = df_groups[df_groups["ID"].isin(user_group_ids)]
        st.subheader("Your Groups")
        if not user_groups_df.empty:
            st.table(user_groups_df)
        else:
            st.info("You are not part of any groups.")