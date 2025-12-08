import streamlit as st
import requests
import pandas as pd
from datetime import date
from get_api import *

def chech_password(password) -> bool:
    if len(password) < 9:
        return False
    lower = any(ch.islower() for ch in password)
    upper = any(ch.isupper() for ch in password)
    number = any(ch.isdigit() for ch in password)
    special = any(not ch.isalnum() for ch in password)

    return lower and upper and number and special

@st.dialog("Make a new account")
def create_user():
    df_users = get_db("users")

    name = st.text_input("Name", placeholder="This field is required")
    second_name = st.text_input("Second name")
    surname = st.text_input("Surname", placeholder="This field is required")
    username = st.text_input("Username", placeholder="This field is required")
    email = st.text_input("Email", placeholder="This field is required")
    password = st.text_input("Password", type="password", placeholder="This field is required")

    if st.button("Submit", key="Submit user"):
        if (df_users["Username"].str.lower() == username).any():
            st.error("This username is taken")
        elif(chech_password(password) == False):
            st.error("Your password should contain at least: 10 characters, a number, a special character, a small and a big letter")
        else:
            if not name.strip() or not surname.strip() or not username.strip() or not email.strip():
                st.error("Please fill in required fields")
            else:
                id = int(df_users["ID"].max() + 1) if not df_users.empty else 1
                data1 = {
                    "id" : id,
                    "name": name,
                    "second_name": second_name,
                    "surname": surname,
                    "username": username,
                    "email": email,
                    "creation_date": date.today().isoformat()
                }

                response = requests.post("http://127.0.0.1:8000/users/", json=data1)

                if response.status_code == 200:
                    st.success("User created successfully!")
                    #st.json(response.json())
                else:
                    st.error("Failed to create user")
                    st.write(response.text)

                data2 = {
                    "user_id" : id,
                    "password": password
                }

                response = requests.post("http://127.0.0.1:8000/passwords/", json=data2)

                if response.status_code != 200:
                    st.error("Internal error")
                    st.write(response.text)


@st.dialog("Make a new account")
def create_account(user_id):
    df_accounts = get_db("accounts")
    account_id = int(df_accounts["ID"].max() + 1) if not df_accounts.empty else 1
    name = st.text_input("Name", placeholder="This field is required")
    type = st.selectbox("Account type:", options=["Personal", "Savings", "Currency"])
    if (type == "Currency"):
        currency = st.selectbox("Currency:", options=["PLN", "EUR", "GBP", "USD", "CZK", "JPY"]) #add more currencies!!!!!!!!!!!
    else:
        currency = "PLN"

    if st.button("Submit", key="Submit account"):
        if not name.strip():
            st.error("Please fill in required fields")
        else:
            data = {
                "id" : account_id,
                "user_id": int(user_id),
                "name": name,
                "type": type,
                "balance": 100,
                "creation_date": date.today().isoformat(),
                "currency": currency
            }

            response = requests.post("http://127.0.0.1:8000/accounts/", json=data)

            if response.status_code == 200:
                st.success("Account created successfully!")
            else:
                st.error("Failed to create an account")
                st.write(response.text)


@st.dialog("Sent a transaction")
def create_transaction(user_id):
    df_transactions = get_db("transactions")
    id = int(df_transactions["ID"].max() + 1) if not df_transactions.empty else 1
    data = fetch_data(f"http://127.0.0.1:8000/accounts/{user_id}")
    accounts = pd.DataFrame(data, columns=["ID", "User ID", "Name", "Type", "Balance", "Created at", "Currency"])
    account = st.selectbox("From account:", options=accounts["Name"])
    if not account:
        st.warning("You have no accounts")
    else:
        chosen_account = accounts[accounts["Name"] == account]
        balance = float(chosen_account["Balance"].iloc[0])
        if(balance <= 0):
                st.warning("Insufficient funds in chosen account")
        else:
            amount= st.number_input("Amount:", min_value=0.01, max_value=float(balance))

            df_users = get_db("users")
            reciever = st.text_input("To user", placeholder="This field is required")
            reciever = df_users[df_users["Username"] == reciever.lower()]

            description = st.text_input("Description")
            if st.button("Sent", key="send transaction"):
                if not amount:
                    st.error("Please fill in required fields")
                elif reciever.empty:
                    st.error("Such user doesn't exists")
                else:
                    data1 = {
                        "id": id,
                        "from_account_id": int(chosen_account["ID"]),
                        "to_account_id": int(reciever["ID"].iloc[0]),
                        "amount": -amount, 
                        "currency": str(chosen_account["Currency"].iloc[0]),
                        "category": "idk",
                        "description": description,
                        "transaction_at": date.today().isoformat(),
                        "created_at": date.today().isoformat()
                    }

                    response = requests.post("http://127.0.0.1:8000/transactions/", json=data1)

                    if response.status_code == 200:
                        st.success("Transaction send!")
                    else:
                        st.error("Failed to sent the transaction")
                        st.write(response.text)

                    data2 = {
                        "id": id + 1,
                        "from_account_id": int(reciever["ID"].iloc[0]),
                        "to_account_id": int(chosen_account["ID"]),
                        "amount": amount, 
                        "currency": str(chosen_account["Currency"].iloc[0]),
                        "category": "idk",
                        "description": description,
                        "transaction_at": date.today().isoformat(),
                        "created_at": date.today().isoformat()
                    }

                    response = requests.post("http://127.0.0.1:8000/transactions/", json=data2)

                    if response.status_code != 200:
                        st.error("Internal error")
                        st.write(response.text)


@st.dialog("Make a new group")
def create_group(user_id, df_groups):
    name = st.text_input("Name", placeholder="This field is required", key="group_name")
    group_id = int(df_groups["ID"].max() + 1) if not df_groups.empty else 1
    if st.button("Submit", key="Submit group"):
        if not name.strip():
            st.error("Please fill in required fields")
        else:
            data1 = {
                "id": group_id,
                "name": name,
                "owner_user_id": int(user_id),
                "created_at": date.today().isoformat()
            }

            response = requests.post("http://127.0.0.1:8000/groups/", json=data1)
            if response.status_code == 200:
                st.success("Group made!")
            else:
                st.error("Failed to create the group")
                st.write(response.text)

            data2 = {
                "user_id": int(user_id),
                "group_id": group_id,
                "role": "Owner",
                "joined_at": date.today().isoformat()
            }

            response = requests.post("http://127.0.0.1:8000/user_groups/", json=data2)
            if response.status_code != 200:
                st.error("Internal error")
                st.write(response.text)


@st.dialog("Add a member")
def create_member(group_id):
    df_users = get_db("users")
    username = st.text_input("Username", placeholder="This field is recuired")
    role = st.text_input("Role", placeholder="This field is recuired")
    new_member = df_users[df_users["Username"].str.lower() ==  username]

    if st.button("Submit", key="Submit member"):
        if not username.strip() or not role.strip():
            st.error("Please fill in required fields")
        elif new_member.empty:
            st.warning("Username not found :(")
        else:
            new_member_id = new_member.iloc[0]["ID"]
            response = requests.get(f"http://127.0.0.1:8000/users/{new_member_id}/groups")
            user_groups = pd.DataFrame(response.json()["groups"], columns=["ID", "User ID", "Group name", "Owned by", "Role", "Created at"])
            if not user_groups.empty and group_id in user_groups["ID"].values:
                st.error("This user is already a member of this group")
            else:
                data = {
                    "user_id": int(new_member["ID"].iloc[0]),
                    "group_id": int(group_id),
                    "role": role,
                    "joined_at": date.today().isoformat()
                }

                response = requests.post("http://127.0.0.1:8000/user_groups/", json=data)
                if response.status_code == 200:
                    st.success("Member added!")
                else:
                    st.error("Failed to add a member")
                    st.write(response.text)


@st.dialog("Sent a group transaction")
def create_group_transaction(user_id, group_id):
    df_group_transactions = get_db("group_transactions")
    df_accounts = get_db("accounts")
    user_accounts_df = df_accounts[df_accounts["User ID"] == user_id]
    account = st.selectbox("Choose account:", options=user_accounts_df["Name"])
    
    if not account:
        st.warning("You have no accounts")
    else:
        chosen_account = df_accounts[df_accounts["Name"] == account]
        balance = float(chosen_account["Balance"].iloc[0])
        if(balance <= 0):
            st.warning("Insufficient funds in chosen account")
        else:
            amount= st.number_input("Amount:", min_value=0.01, max_value=float(balance))
            description = st.text_input("Despription")
            if st.button("Sent", key="Submit group transaction"):
                    data = {
                        "id": int(df_group_transactions["ID"].max() + 1) if not df_group_transactions.empty else 1,
                        "group_id": int(group_id),
                        "paid_by_user_id": int(user_id),
                        "amount": float(amount),
                        "currency": str(chosen_account["Currency"].iloc[0]),
                        "description": description,
                        "created_at": date.today().isoformat()
                    }

                    response = requests.post("http://127.0.0.1:8000/group_transactions/", json=data)
                    if response.status_code == 200:
                        st.success("Transaction send!")
                    else:
                        st.error("Failed to sent the transaction")
                        st.write(response.text)