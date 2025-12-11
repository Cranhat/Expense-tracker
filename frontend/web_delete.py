import streamlit as st
import requests
from get_api import *

def delete(df: str, id):
    route = APIS[df] + f"/{id}"
    response = requests.delete(route)
    if response.status_code != 200:
        st.write(response.text)

def delete_user(user_id):
    delete("users", user_id)
    delete("passwords", user_id)

    df_accounts = get_db("accounts")
    accounts_to_delete = df_accounts[df_accounts["User ID"] == user_id]
    for _, row in accounts_to_delete.iterrows():
        delete_account(row["ID"])

    df_groups = get_db("groups")
    groups_to_delete = df_groups[df_groups["Owned by"] == user_id]
    for _, row in groups_to_delete.iterrows():
        delete_group(row["ID"])
    
    st.rerun()

def delete_account(account_id):
    delete("accounts", account_id)
    df_transactions = get_db("transactions")

    transactions_to_delete = df_transactions[df_transactions["From account ID"] == account_id]
    for _, row in transactions_to_delete.iterrows():
        delete("transactions", row["ID"])

    st.rerun()


def delete_group(group_id):
    delete("groups", group_id)
    df_group_transactions = get_db("group_transactions")
    df_user_group = get_db("user_groups")

    transactions_to_delete = df_group_transactions[df_group_transactions["Group ID"] == group_id]
    for _, row in transactions_to_delete.iterrows():
        delete("group_transactions", row["ID"])

    groups_to_delete = df_user_group[df_user_group["Group ID"] == group_id]
    for _, row in groups_to_delete.iterrows():
        delete("user_groups", row["Group ID"])

    st.rerun()

@st.dialog("Delete a member")
def delete_member(group_id, owner):
    df_users = get_db("users")
    data = fetch_data(f"http://127.0.0.1:8000/groups/{group_id}/data")
    group = pd.DataFrame(data, columns=["User ID", "Username", "Owner", "Owner ID", "Role", "Joined at", "Name"])
    deletable_members = group[group["Username"] != owner]["Username"].tolist()
    username = st.selectbox("Select member", options=deletable_members)
    chosen_member = df_users[df_users["Username"] == username]
    if st.button("Delete", key="Delete member1"):
        user_id = int(chosen_member["ID"])
        route = f"http://127.0.0.1:8000/user_groups/{group_id}/{user_id}"
        response = requests.delete(route)
        if response.status_code != 200:
            st.write(response.text)
        st.rerun()

###########################################################

def request_delete():
    st.session_state.show_delete_confirm = True
    st.rerun()

def confirm_delete():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.show_delete_confirm = False

def cancel_delete():
    st.session_state.show_delete_confirm = False
    st.rerun()

@st.dialog("Delete user")
def delete_user_dialog(user_id):
    st.write("Are you sure you want to delete your user from the service?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, delete", type="primary"):
            #delete_user(user_id)
            confirm_delete()
            delete_user(user_id)
    with col2:
        if st.button("No, go back"):
            cancel_delete()
            st.rerun

