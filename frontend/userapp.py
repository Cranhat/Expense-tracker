import streamlit as st
import requests
import pandas as pd
from datetime import date

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

acc_map_to_type = {
    "Personal": 1,
    "Savings": 2,
    "Currency": 3
}

acc_map_from_type = {
    1 : "Personal",
    2 : "Savings",
    3 : "Currency"
}

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

        if "df_users" not in st.session_state:
            st.session_state.df_users = df_users.copy()
        if "df_accounts" not in st.session_state:
            st.session_state.df_accounts = df_accounts.copy()
        if "df_transactions" not in st.session_state:
            st.session_state.df_transactions = df_transactions.copy()

        # new account
        with st.expander("Add a New Account"):
            account_name = st.text_input("Account Name:", key="account_new_account")
            account_type = st.selectbox("Account type:", options=["Personal", "Savings", "Currency"])
            account_type = acc_map_to_type[account_type]
            if (account_type == 3):
                account_currency = st.selectbox("Currency:", options=["PLN", "EUR"]) #add more currencies!!!!!!!!!!!
            else:
                account_currency = "PLN"
            if st.button("Create Account", key=f"create_{user_id}"):
                new_account = {
                    "ID": st.session_state.df_accounts["ID"].max() + 1 if not df_accounts.empty else 1,
                    "User ID": user_id,
                    "Name": account_name,
                    "Type" : account_type,
                    "Balance": 0.00,
                    "Created at": date.today(),
                    "Currency": account_currency
                }
                st.session_state.df_accounts = pd.concat([st.session_state.df_accounts, pd.DataFrame([new_account])], ignore_index=True)
                st.success(f"Account '{account_name}' created successfully!")

        # acoounts
        user_accounts_df = st.session_state.df_accounts[st.session_state.df_accounts["User ID"] == user_id]
        display_user_accounts_df = user_accounts_df.drop(columns=["ID", "User ID"])
        display_user_accounts_df["Type"] = display_user_accounts_df["Type"].map(acc_map_from_type)
        st.subheader("Your Accounts")
        if not user_accounts_df.empty:
            st.table(display_user_accounts_df) #accounts table
            account_to_show = None

            
            with st.expander("Show transactions"):
                for idx, row in user_accounts_df.iterrows():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        type_str = acc_map_from_type.get(row['Type'], "Unknown")
                        st.write(f"{row['Name']} - Type: {type_str} - Balance: {row['Balance']}")
                    with col2:
                        if st.button("Load Transactions", key=f"txn_{row['ID']}"):
                            account_to_show = row['ID']


            if account_to_show is not None:
                st.subheader("Transactions")
                show_transactions = st.session_state.df_transactions[st.session_state.df_transactions["Account ID"] == account_to_show]
                show_transactions = show_transactions.drop(columns=["ID", "From account ID", "Account ID"])
                st.dataframe(show_transactions, use_container_width=True) #transactions table

                # submitted = 0
                # with st.expander("Add a transaction"):
                #     with st.form("add_transaction_form"):
                #         to_username = st.text_input("To user:", key="txn_to_user").strip().lower()
                #         to_user = st.session_state.df_users[
                #             st.session_state.df_users["Username"].str.lower() == to_username
                #         ]
                #         st.button("Check user")
                #         if to_username and to_user.empty:
                #             st.info("No such user")
                #         if not to_user.empty:
                #             receiver_user_id = int(to_user.iloc[0]["ID"])

                #             possible_accounts = st.session_state.df_accounts[st.session_state.df_accounts["User ID"] == receiver_user_id]
                #             if possible_accounts.empty:
                #                 st.info("That user has no accounts")
                #             else:
                #                 receiver_account_name = st.selectbox("Receiver account:",options=possible_accounts["Name"])
                #                 receiver_account = possible_accounts[possible_accounts["Name"] == receiver_account_name].iloc[0]            
                #                 sender_account = st.session_state.df_accounts[st.session_state.df_accounts["ID"] == account_to_show].iloc[0]
                #                 amount = st.number_input("Amount:", min_value=0.01, max_value=sender_account["Balance"])
                #                 description = st.text_input("Description:")

                #         submitted = st.form_submit_button("Create transaction")
                #     if submitted:
                #                     new_id = ( st.session_state.df_transactions["ID"].max() + 1 if not st.session_state.df_transactions.empty else 1 )

                #                     new_transaction = {
                #                         "ID": new_id,
                #                         "From account ID": sender_account["ID"],
                #                         "Account ID": receiver_account["ID"],   # FIXED
                #                         "Amount": -amount,                      # negative for sender
                #                         "Currency": sender_account["Currency"],
                #                         "Category": 0,
                #                         "Description": description,
                #                         "Transaction at": date.today(),
                #                         "Created at": date.today(),
                #                     }

                #                     st.session_state.df_transactions = pd.concat([st.session_state.df_transactions,pd.DataFrame([new_transaction]),],ignore_index=True,)
                #                     st.success("Transaction created successfully!")


        # groups
        user_group_ids = df_user_groups[df_user_groups["User ID"] == user_id]["Group ID"].tolist()
        user_groups_df = df_groups[df_groups["ID"].isin(user_group_ids)]
        st.subheader("Your Groups")
        if not user_groups_df.empty:
            st.table(user_groups_df)
        else:
            st.info("You are not part of any groups.")