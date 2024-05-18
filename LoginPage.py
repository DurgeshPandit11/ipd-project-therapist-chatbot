import streamlit as st
from ChatbotApp import chatbot_app

# Initialize connection
conn = st.connection('mysql', type='sql')

# Initialize container for login
login_container = st.container()

# Initializing "login_successful" session variable
if 'login_successful' not in st.session_state:
    st.session_state['login_successful'] = False

def check_credentials(username: str, password: str):
    query = 'SELECT user_id FROM user_login WHERE username = "{}" AND user_password = "{}";'.format(username, password)
    df = conn.query(query)
    if len(df) == 1:
        st.success("Success")
        st.session_state["user_id"] = df["user_id"][0]
        st.session_state["login_successful"] = True
    else:
        st.error("Login Failed")

def show_login_container():
    with login_container:
        st.title("Login")
        if st.session_state['login_successful'] == False:
            username = st.text_input(label="Username:", placeholder="Username", max_chars=50)
            password = st.text_input(label="Password:", placeholder="Password", type="password")
            st.button("Login", on_click=check_credentials(username, password))

if st.session_state["login_successful"] == False:
    show_login_container()
else:
    chatbot_app()