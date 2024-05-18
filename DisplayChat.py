import streamlit as st
import json

conn = st.connection("mysql", type="sql")

def display_chat(userid: int, date: str):
    query = "SELECT messages FROM Chats WHERE user_id = {} AND chat_date = '{}'".format(userid, date)
    df = conn.query(query)
    
    messages = df["messages"][0]
    
    messages = messages.replace("''", "'")

    messages = json.loads(messages)

    # Display chat messages
    st.write("Date:", date)
    st.write("Messages:")
    for message in messages[1:]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

display_chat(1, "2024-04-27")