import streamlit as st

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