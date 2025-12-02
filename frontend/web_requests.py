import streamlit as st
import requests
from datetime import date

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

def create_user(id):
    with st.expander("Create User"):
        name = st.text_input("Name", placeholder="This field is required")
        second_name = st.text_input("Second name")
        surname = st.text_input("Surname", placeholder="This field is required")
        username = st.text_input("Username", placeholder="This field is required")
        email = st.text_input("Email", placeholder="This field is required")

        if st.button("Submit"):
            if not name.strip() or not surname.strip() or not username.strip() or not email.strip():
                st.error("Please fill in required fields")
            else:
                data = {
                    "id" : id,
                    "name": name,
                    "second_name": second_name,
                    "surname": surname,
                    "username": username,
                    "email": email,
                    "creation_date": date.today().isoformat()
                }

                response = requests.post("http://127.0.0.1:8000/users/", json=data)

                if response.status_code == 200:
                    st.success("User created successfully!")
                    #st.json(response.json())
                else:
                    st.error("Failed to create user")
                    st.write(response.text)


def create_account(user_id, account_id):
    with st.expander("Add a new account"):
        name = st.text_input("Name", placeholder="This field is required")
        type = st.selectbox("Account type:", options=["Personal", "Savings", "Currency"])
        if (type == "Currency"):
            currency = st.selectbox("Currency:", options=["PLN", "EUR"]) #add more currencies!!!!!!!!!!!
        else:
            currency = "PLN"

        if st.button("Submit"):
            if not name.strip():
                st.error("Please fill in required fields")
            else:
                data = {
                    "id" : account_id,
                    "user_id": user_id,
                    "name": name,
                    "type": type,
                    "balance": 0.00,
                    "creation_date": date.today().isoformat(),
                    "currency": currency
                }

                response = requests.post("http://127.0.0.1:8000/accounts/", json=data)

                if response.status_code == 200:
                    st.success("Account created successfully!")
                else:
                    st.error("Failed to create an account")
                    st.write(response.text)


def create_transaction(id, receiver_id, account):
    with st.expander("Add a new transaction"):
        amount = st.number_input("Amount:", min_value=0.01, max_value=account["Balance"])
        description = st.text_input("description")

        if st.button("Submit"):
            if not amount:
                st.error("Please fill in required fields")
            else:
                data = {
                    "if": id,
                    "from_account_id": int(account["ID"]),
                    "to_account_id": receiver_id,
                    "amount": -amount, 
                    "currency": str(account["Currency"]),
                    "category": "idk",
                    "description": description,
                    "transaction_at": date.today().isoformat(),
                    "created_at": date.today().isoformat()
                }


                response = requests.post("http://127.0.0.1:8000/transactions/", json=data)

                if response.status_code == 200:
                    st.success("Transaction send!")
                else:
                    st.error("Failed to send the transaction")
                    st.write(response.text)
