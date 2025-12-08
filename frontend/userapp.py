import streamlit as st
import pandas as pd
from get_api import *
from web_requests import *
from log_handler import *

st.title("Personal Expense Tracker")

#               -Session states-              
##############################################

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "show_logout_confirm" not in st.session_state:
    st.session_state.show_logout_confirm = False
if "manage_group" not in st.session_state:
    st.session_state.manage_group = -1
if "user_id" not in st.session_state:
    st.session_state.user_id = -1

##############################################

df_users = get_db("users")


#               -Logging in-           
##############################################
if not st.session_state.logged_in:
    #username_input = st.text_input("Enter your username", value="")
    #password_input = st.text_input("Enter your password", type="password", value="")
    username_input = "naitomi"
    password_input = "aaaaaaaaaaaaA123!"
    if st.button("Log in"):
            if not username_input.strip() or not password_input.strip():
                st.warning("Please fill in required fields")
            else:
                df_user = df_users[df_users["Username"].str.lower() ==  username_input]
                if df_user.empty:
                    st.warning("Username not found")
                else:
                    id = df_user.iloc[0]["ID"]
                    data =fetch_data(f"http://127.0.0.1:8000/passwords/{id}")
                    password = pd.DataFrame(data, columns=["ID", "Password"])
                    if(password["Password"].iloc[0] != password_input):
                        st.error("Wrong password")
                    else:
                        do_login(username_input.strip().lower())
##############################################



#               -Running session-           
##############################################
if st.session_state.logged_in and st.session_state.manage_group == -1:

    df_accounts = get_db("accounts")
    df_transactions = get_db("transactions")
    df_groups = get_db("groups")
    df_user_groups = get_db("user_groups")

    df_user = df_users[df_users["Username"].str.lower() ==  st.session_state.username]


    user_id = df_user.iloc[0]["ID"]
    first_name = df_user.iloc[0]["First name"]
    st.subheader(f"Welcome, {first_name}!")

    # new account
    create_account(int(df_user["ID"].iloc[0]), int(df_accounts["ID"].max() + 1) if not df_accounts.empty else 1)
    df_accounts = get_db("accounts")

    # acoounts
    user_accounts_df = df_accounts[df_accounts["User ID"] == user_id]
    display_user_accounts_df = user_accounts_df.drop(columns=["ID", "User ID"])
    st.subheader("Your Accounts")
    if not user_accounts_df.empty:
        st.table(display_user_accounts_df) #accounts table
        account_to_show = None
        
        with st.expander("Show transactions"):
            for idx, row in user_accounts_df.iterrows():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{row['Name']} - Type: {row['Type']} - Balance: {row['Balance']}")
                with col2:
                    if st.button("Load Transactions", key=f"txn_{row['ID']}"):
                        account_to_show = row['ID']


        if account_to_show is not None:
            st.subheader("Transactions")
            show_transactions = df_transactions[df_transactions["Account ID"] == account_to_show]
            show_transactions = show_transactions.drop(columns=["ID", "From account ID", "Account ID"])
            st.dataframe(show_transactions, width='stretch') #transactions table

    # groups
    response = requests.get(f"http://127.0.0.1:8000/users/{user_id}/groups")
    user_groups = pd.DataFrame(response.json()["groups"], columns=["ID", "User ID", "Group name", "Owned by", "Role", "Created at"])
    df_groups = get_db("groups")

    st.subheader("Your Groups")
    if not user_groups.empty:
        st.table(user_groups.drop(columns=["ID", "User ID",]))
    else:
        st.info("You are not part of any groups.")

    create_group(user_id, df_groups)
    with st.expander("Manage your groups"):
        for idx, row in user_groups.iterrows():
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"{row['Group name']}")
            with col2:
                if st.button("Manage", key=f"manage_{row['ID']}"):
                    st.session_state.manage_group = row["ID"]
                    st.session_state.user_id = user_id

    if not st.session_state.show_logout_confirm:
        if st.button("Log out"):
            request_logout()
    else:
        logout_dialog()
##############################################



#               -Group management-           
##############################################
if st.session_state.manage_group != -1:
    group_id = st.session_state.manage_group
    st.text(group_id)
    data = fetch_data(f"http://127.0.0.1:8000/groups/{group_id}/data")
    group = pd.DataFrame(data, columns=["User ID", "Username", "Owner", "Owner ID", "Role", "Joined at", "Name"])
    owner = group.at[0, "Owner"]
    group_name = group["Name"].iloc[0]
    if st.session_state.user_id == group["Owner ID"].iloc[0]:
        text = owner
    else:
        text = "you"

    data = fetch_data(f"http://127.0.0.1:8000/group_transactions/{group_id}")
    group_transactions = pd.DataFrame(data, columns=["ID", "Group ID", "Paid by", "Amount", "Currency", "Description", "Created at"])

    st.subheader(f"Managing group {group_name}, owned by {text}")
    st.text("Members")
    st.table(group.drop(columns=["User ID", "Owner", "Owner ID", "Name"]))
    if st.session_state.user_id == group["Owner ID"].iloc[0]:
        with st.expander("Add a member"):
            create_member(group_id)
    st.table(group_transactions.drop(columns=["ID", "Group ID"]))
    with st.expander("Make a new transaction"):
        create_group_transaction(st.session_state.user_id, group_id)

    if st.button("Go back"):
        st.session_state.manage_group = -1
##############################################


if st.session_state.logged_in is False:
    create_user()


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
