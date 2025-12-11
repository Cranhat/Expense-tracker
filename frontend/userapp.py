import streamlit as st
import pandas as pd
from get_api import *
from web_requests import *
from log_handler import *
from web_delete import *
from backend.app.database.password_encryption import *

st.title("Personal Expense Tracker")

#               -Session states-              
##############################################

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "show_logout_confirm" not in st.session_state:
    st.session_state.show_logout_confirm = False
if "show_delete_confirm" not in st.session_state:
    st.session_state.show_delete_confirm = False
if "manage_group" not in st.session_state:
    st.session_state.manage_group = -1
if "user_id" not in st.session_state:
    st.session_state.user_id = -1
if "text_flag" not in st.session_state:
    st.session_state.text_flag = 0
if "text" not in st.session_state:
    st.session_state.text = ""
##############################################

df_users = get_db("users")


#               -Logging in-           
##############################################
if not st.session_state.logged_in:
    username_input = st.text_input("Enter your username", value="")
    password_input = st.text_input("Enter your password", type="password", value="")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Log in", width='stretch'):
                if not username_input.strip() or not password_input.strip():
                    st.warning("Please fill in required fields", width=1000)
                else:
                    df_user = df_users[df_users["Username"].str.lower() ==  username_input]
                    if df_user.empty:
                        st.warning("Username not found")
                    else:
                        id = df_user.iloc[0]["ID"]
                        data =fetch_data(f"http://127.0.0.1:8000/passwords/{id}")
                        password = pd.DataFrame(data, columns=["ID", "Password"])
                        if password.empty:
                            st.error("Wrong password")
                        elif(not verify_password(password_input, password["Password"].iloc[0])):
                            st.error("Wrong password")
                        else:
                            do_login(username_input.strip().lower())
    with col2:
        if st.button("Sign in", width='stretch'):
            create_user()
##############################################



#               -Running session-           
##############################################
if st.session_state.logged_in and st.session_state.manage_group == -1:

    if st.session_state.text_flag == 1:
        st.success(st.session_state.text)
    if st.session_state.text_flag == -1:
        st.error(st.session_state.text)

    df_user = df_users[df_users["Username"].str.lower() ==  st.session_state.username]
    user_id = df_user.iloc[0]["ID"]
    first_name = df_user.iloc[0]["First name"]
    st.subheader(f"Welcome, {first_name}!")

    # text:
    # 1 - success
    # 0 - text
    # -1 - error

    # buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Make a new account", width='stretch'):
            create_account(user_id)
    with col2:
        if st.button("Make a new transaction", width='stretch'):
            create_transaction(user_id)
    with col3:
        if st.button("Make a new group", width='stretch'):
            create_group(user_id)

    

    # acoounts
    df_accounts = get_db("accounts")
    user_accounts_df = df_accounts[df_accounts["User ID"] == user_id]
    display_user_accounts_df = user_accounts_df.drop(columns=["ID", "User ID"])
    st.subheader("Your Accounts")
    if not user_accounts_df.empty:
        st.dataframe(display_user_accounts_df) #accounts table
        account_to_show = None
        
        with st.expander("Manage accounts"):
            for idx, row in user_accounts_df.iterrows():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                with col1:
                    st.write(f"{row['Name']} - Type: {row['Type']} - Balance: {row['Balance']}")
                with col2:
                    if st.button("Load Transactions", key=f"txn_{row['ID']}", width='stretch'):
                        account_to_show = row['ID']
                with col3:
                    if st.button("Deposit", width='stretch'):
                        deposit(row['ID'])
                with col4:
                     if st.button("Delete", key=f"delete_account_{row['ID']}", width='stretch', type='primary'):
                        delete_account(row['ID'])

        #transactions
        if account_to_show is not None:
            df_transactions = get_db("transactions", account_to_show)
            st.subheader("Transactions")
            st.dataframe(df_transactions.drop(columns=["ID", "From account ID", "To account ID"]), width='stretch') #transactions table
    else:
         st.info("You have no accounts")

    # groups
    response = requests.get(f"http://127.0.0.1:8000/users/{user_id}/groups")
    user_groups = pd.DataFrame(response.json()["groups"], columns=["ID", "User ID", "Group name", "Owned by", "Role", "Created at"])
    df_groups = get_db("groups")

    st.subheader("Your Groups")
    if not user_groups.empty:
        st.dataframe(user_groups.drop(columns=["ID", "User ID",]))

        with st.expander("Manage your groups"):
            for idx, row in user_groups.iterrows():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"{row['Group name']}")
                with col2:
                    if st.button("Manage", width='stretch', key=f"manage_{row['ID']}"):
                        st.session_state.manage_group = row["ID"]
                        st.session_state.user_id = user_id
                        st.rerun()
                with col3:
                    if st.button("Delete group", key=f"delete_group_{row['ID']}", width='stretch', type='primary'):
                            delete_group(row['ID'])
    else:
        st.info("You are not part of any groups.")

    col1, col2 = st.columns(2)
    with col1:

        if not st.session_state.show_logout_confirm:
            if st.button("Log out", type='primary', width='stretch'):
                request_logout()
        else:
            logout_dialog()

    with col2:
        if not st.session_state.show_delete_confirm:
            if st.button("Delete user", type='primary', width='stretch'):
                request_delete()
        else:
            delete_user_dialog(user_id)
##############################################



#               -Group management-           
##############################################
if st.session_state.manage_group != -1:

    if st.session_state.text_flag == 1:
        st.success(st.session_state.text)
    if st.session_state.text_flag == -1:
        st.error(st.session_state.text)

    group_id = st.session_state.manage_group
    data = fetch_data(f"http://127.0.0.1:8000/groups/{group_id}/data")
    group = pd.DataFrame(data, columns=["User ID", "Username", "Owner", "Owner ID", "Role", "Joined at", "Name"])
    if not group.empty:
        owner = group.iloc[0]["Owner"]
        group_name = group["Name"].iloc[0]
        if st.session_state.user_id == group["Owner ID"].iloc[0]:
            text = "you"
        else:
            text = owner

        st.subheader(f"Managing group \"{group_name}\", owned by {text}")
        st.text("Members", width='content')
        st.table(group.drop(columns=["User ID", "Owner", "Owner ID", "Name"]))
        st.text("Transactions")
        group_transactions = get_db("group_transactions", group_id)
        st.table(group_transactions.drop(columns=["ID", "Group ID"]))

        if st.session_state.user_id == group["Owner ID"].iloc[0]:
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Add a member", width='stretch'):
                    create_member(group_id)
            with col2:
                if st.button("Make a new transaction", width='stretch', key="new group transaction admin"):
                    create_group_transaction(st.session_state.user_id, group_id)
            with col3:
                if st.button("Delete a member", width='stretch', type='primary'):
                    delete_member(group_id, owner)
        else:
            if st.button("Make a new transaction", key="new group transaction"):
                create_group_transaction(st.session_state.user_id, group_id)

        if st.button("Go back"):
            st.session_state.manage_group = -1
            st.rerun()
##############################################
st.session_state.text_flag = 0