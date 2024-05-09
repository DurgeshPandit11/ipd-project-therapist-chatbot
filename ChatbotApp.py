import streamlit as st
from openai import OpenAI
import os
import json
from DisplayChat import display_chat
from NewChat import new_chat

# Note: Will crash if 1st character of message is "

# App title
# st.set_page_config(page_title="Digital Therapist")

conn = st.connection("mysql", type="sql")

def get_dates_list_from_db():
    query = "SELECT chat_date FROM Chats WHERE user_id = {} ORDER BY chat_date DESC;".format(st.session_state["user_id"])
    chat_dates = conn.query(query)
    dates = []

    for date in chat_dates.itertuples():
        dates.append(date.chat_date)
    
    return dates

def current_day_session_in_db():
    query = "SELECT COUNT(1) AS today_date_in_db FROM Chats WHERE user_id = {} AND chat_date = NOW() ORDER BY chat_date DESC;".format(st.session_state["user_id"])
    df = conn.query(query)
    # st.write(df)
    return df["today_date_in_db"][0]


# get_dates_list_from_db()
# display_historical_chat(1, "2024-04-27")
# chatbot_app()

# # Disable the "end session" button and "chat_input" after "end session" button is clicked
# def end_session():
#     st.session_state["session_ended"] = True
    
# def get_session_messages():
#     return st.session_state["messages"]

# # Initialize disabled for __ to False
# if "session_ended" not in st.session_state:
#     st.session_state["session_ended"] = False

# # def current_day_session():


def chatbot_app():
    # Sidebar
    with st.sidebar:
        st.title("Digital Therapist")
        date = st.selectbox(label="Chat History:", options=get_dates_list_from_db(), placeholder="Choose a Date")
        # st.button(
        #     "End Session",
        #     # key="end_session",
        #     # on_click=end_session,
        #     # disabled=st.session_state["session_ended"]
        # )
        # # if st.session_state["session_ended"]:
        # #     st.write("Session Ended")
    # st.title("Digital Therapist")
    
    # display_chat(st.session_state["user_id"], date)
    new_chat()

    # if current_day_session_in_db():
    #     st.write("Show History")
    # else:
    #     st.write("Show new chat area")


# # Sidebar
# with st.sidebar:
#     st.title("Digital Therapist")
#     st.button(
#         "End Session", 
#         # key="end_session",
#         on_click=end_session,
#         disabled=st.session_state["session_ended"]
#     )

#     if st.session_state["session_ended"]:
#         st.write("Session Ended")
#         # st.button("View Report")

# # Store LLM generated responses
# system_msg = "You are a therapist chatbot. The user will describe their feelings or situation to you. Respond to them as a therapist and continue the session by asking the next question."

# if "messages" not in st.session_state.keys():
#     st.session_state.messages = [
#         {"role": "system", "content": system_msg},
#         {"role": "assistant", "content": "Welcome! How are you feeling today?"}
#     ]

# # Display chat messages
# for message in st.session_state.messages[1:]:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

# # Function for generating chatbot response
# client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

# def generate_chatbot_response():
#         response_obj = client.chat.completions.create(
#             model = "ft:gpt-3.5-turbo-0125:personal:therapistbot-2:9AMcj2pW",
#             messages = st.session_state["messages"],
#             temperature=0.5,
#             # top_p=1,
#         )
#         response_text = response_obj.choices[0].message.content
#         return response_text

# # User-provided prompt
# if prompt := st.chat_input(disabled=st.session_state["session_ended"]):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.write(prompt)

# # Generate a new response if last message is not from assistant
# if st.session_state.messages[-1]["role"] != "assistant":
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             chatbot_response = generate_chatbot_response()
#             placeholder = st.empty()
#             placeholder.markdown(chatbot_response)
#     st.session_state["messages"].append({"role": "assistant", "content": chatbot_response})

# # st.write(st.session_state["messages"])