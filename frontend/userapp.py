import streamlit as st
import requests
import pandas as pd
from datetime import date
from get_api import *
from web_requests import *

st.title("Personal Expense Tracker")

df_users, df_accounts, df_transactions, df_groups, df_user_groups, df_group_transactions = get_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "show_logout_confirm" not in st.session_state:
    st.session_state.show_logout_confirm = False

def do_login(name: str):
    if name:
        st.session_state.username = name
        st.session_state.logged_in = True
        st.session_state.show_logout_confirm = False
        st.rerun()

def request_logout():
    st.session_state.show_logout_confirm = True
    st.rerun()

def confirm_logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.show_logout_confirm = False
    st.rerun()

def cancel_logout():
    st.session_state.show_logout_confirm = False
    st.rerun()

@st.dialog("Confirm Logout")
def logout_dialog():
    st.write("Are you sure you want to log out?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, log out", type="primary"):
            confirm_logout()
    with col2:
        if st.button("No, stay"):
            cancel_logout()


if not st.session_state.logged_in:
    username_input = st.text_input("Enter your username", value="")
    if st.button("Log in"):
            do_login(username_input.strip().lower())

if st.session_state.logged_in:
    df_user = df_users[df_users["Username"].str.lower() ==  st.session_state.username]

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
        create_account(int(df_user["ID"].iloc[0]), int(df_accounts["ID"].max() + 1) if not df_accounts.empty else 1)

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


        if not st.session_state.show_logout_confirm:
            if st.button("Log out"):
                request_logout()
        else:
            logout_dialog()
            # st.warning("Are you sure you want to log out?")
            # col1, col2 = st.columns(2)
            # with col1:
            #     if st.button("Yes, log out"):
            #         confirm_logout()
            # with col2:
            #     if st.button("Cancel"):
            #         cancel_logout()


if st.session_state.logged_in is False:
    create_user(int(df_users["ID"].max() + 1) if not df_users.empty else 1)