import streamlit as st
from openai import OpenAI
import os
import json
import mysql.connector
import GetReport
from GetChatSummary import get_conversation_str, get_summary
import matplotlib.pyplot as plt
from DisplayChat import display_chat

# from DisplayChat import display_chat
# from NewChat import new_chat

# Note: Will crash if 1st character of message is "

# App title
# st.set_page_config(page_title="Digital Therapist")

# Initialize streamlit connection
conn = st.connection("mysql", type="sql")

# Initialize mysql.connector connection
ipd_db_conn = mysql.connector.connect(
  host="localhost",
	user="root",
	password="Mysql@123",
	database="ipd"
)

# DB Cursor
cursor = ipd_db_conn.cursor(buffered = True)

def get_dates_list_from_db():
    query = "SELECT chat_date FROM Chats WHERE user_id = {} ORDER BY chat_date DESC;".format(st.session_state["user_id"])
    chat_dates = conn.query(query)
    dates = []

    for date in chat_dates.itertuples():
        dates.append(date.chat_date)
    
    return dates


def is_current_date_in_db():
    query = "SELECT * FROM Chats WHERE chat_date = DATE(NOW())"
    df = conn.query(query)
    return len(df)


def current_day_session_in_db():
    query = "SELECT COUNT(1) AS today_date_in_db FROM Chats WHERE user_id = {} AND chat_date = NOW() ORDER BY chat_date DESC;".format(st.session_state["user_id"])
    df = conn.query(query)
    # st.write(df)
    return df["today_date_in_db"][0]


# get_dates_list_from_db()
# display_historical_chat(1, "2024-04-27")
# chatbot_app()


# Disable the "end session" button and "chat_input" after "end session" button is clicked
def end_session():
    st.session_state["session_ended"] = True
    
# def get_session_messages():
#     return st.session_state["messages"]

# # def current_day_session():


def new_chat():
    # Store LLM generated responses
    system_msg = "You are a therapist chatbot. The user will describe their feelings or situation to you. Respond to them as a therapist and continue the session by asking the next question."

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "system", "content": system_msg},
            {"role": "assistant", "content": "Welcome! How are you feeling today?"}
        ]

    # Display chat messages
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Function for generating chatbot response
    client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

    def generate_chatbot_response():
        response_obj = client.chat.completions.create(
            model = "ft:gpt-3.5-turbo-0125:personal:therapistbot-2:9AMcj2pW",
            messages = st.session_state["messages"],
            temperature=0.5,
            # top_p=1,
        )
        response_text = response_obj.choices[0].message.content
        return response_text

    # User-provided prompt
    if prompt := st.chat_input(disabled=st.session_state["session_ended"]): # disabled=st.session_state["session_ended"]
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chatbot_response = generate_chatbot_response()
                placeholder = st.empty()
                placeholder.markdown(chatbot_response)
        st.session_state["messages"].append({"role": "assistant", "content": chatbot_response})


# # Initialize disabled for __ to False
# if "session_ended" not in st.session_state:
#     st.session_state["session_ended"] = False

def format_list_of_messages(messages_dict_list: list):
    # Remove double quotes from all messages
    for message_dict in messages_dict_list:
        message_dict["content"] = message_dict["content"].replace('"', "")
    
    # Convert list to string using json.dumps()
    messages_str = json.dumps(messages_dict_list)

    # Replace " with "" and ' with '' in string
    messages_str = messages_str.replace('"', '""')
    messages_str = messages_str.replace("'", "''")

    return messages_str

# def insert_chat_messages_in_db(formatted_messages_str: str):
#     query = 'INSERT INTO chats (user_id, chat_date, messages) VALUES ({}, DATE(NOW()), "{}");'.format(st.session_state["user_id"], formatted_messages_str)
#     # query = 'INSERT INTO Chats (messages) WHERE user_id = {} AND chat_date = DATE(NOW()) VALUES {}'.format(st.session_state["user_id"], st.session_state["messages"])
#     cursor.execute(query)
#     ipd_db_conn.commit()
#     with st.sidebar:
#         st.success("Messages were successfully saved to the database!")

def get_topic_labels_new_chat():
    user_messages_list = GetReport.get_user_messages(st.session_state["messages"])
    topic_labels_list = []
    for message in user_messages_list:
        user_message_vector = GetReport.preprocess_user_message(message)
        topic_labels_list.append(GetReport.predict_tag_for_user_message(user_message_vector)[0]["intent"])
    st.write(topic_labels_list)

    return topic_labels_list

def get_topic_labels_old_chat(user_id: int, date: str):
    query='SELECT topics FROM Chats WHERE user_id = {} AND chat_date = "{}"'.format(user_id, date)
    df = conn.query(query)
    # return df["topics"][0]
    topics = df["topics"][0].replace("''", "'")
    topics = json.loads(topics)
    return topics


def get_formatted_topic_labels_str(topic_labels_list: list):
    # Convert list to string using json.dumps()
    topic_labels_str = json.dumps(topic_labels_list)

    # Replace " with "" and ' with '' in string
    topic_labels_str = topic_labels_str.replace('"', '""')
    topic_labels_str = topic_labels_str.replace("'", "''")

    return topic_labels_str

def insert_data_in_db(formatted_messages_str: str, formatted_topic_labels_str: str, conversation_summary: str):
    query = 'INSERT INTO chats (user_id, chat_date, messages, topics, summary) VALUES ({}, DATE(NOW()), "{}", "{}", "{}");'.format(st.session_state["user_id"], formatted_messages_str, formatted_topic_labels_str, conversation_summary)
    # query = 'INSERT INTO Chats (messages) WHERE user_id = {} AND chat_date = DATE(NOW()) VALUES {}'.format(st.session_state["user_id"], st.session_state["messages"])
    cursor.execute(query)
    ipd_db_conn.commit()
    with st.sidebar:
        st.success("Data was successfully saved to the database!")

def show_report(topic_labels_list):
    detected_topics_list = [topic for topic in topic_labels_list if topic != "unknown"]
    fig = plt.figure(figsize=(6,5))
    plt.title("Topics Detected")
    plt.xlabel("Topic")
    plt.ylabel("Frequency")
    plt.xticks(rotation=90)
    plt.hist(detected_topics_list)
    st.pyplot(fig)
    

def chatbot_app():
    # Getting it right
    # Initialize 
    if "session_ended" not in st.session_state:
        st.session_state["session_ended"] = False
    
    if "new_chat" not in st.session_state:
        st.session_state["new_chat"] = False
    
    
    # Sidebar
    with st.sidebar:
        st.title("Digital Therapist")
        date = st.selectbox(label="Chat History:", options=get_dates_list_from_db(), placeholder="Choose a Date")
        
        # if new chat only then show end session button
        if st.session_state["new_chat"]:
            st.button(
                "End Session",
                # key="end_session",
                on_click=end_session,
                disabled=st.session_state["session_ended"]
            )
        if st.session_state["session_ended"]:
            st.write("Session Ended")
    
    # Logic
    if is_current_date_in_db():
        # st.write("Looks like today's session is over! Here are the messages:")
        display_chat(st.session_state["user_id"], date)
        show_report(get_topic_labels_old_chat(st.session_state["user_id"], date))
    else:
        st.session_state["new_chat"] = True
        new_chat()
    
    # Insert chat in database
    if st.session_state["session_ended"]:
    
        # get required things to put in database
        formatted_msgs_str = format_list_of_messages(st.session_state["messages"])

        topic_labels = get_topic_labels_new_chat()
        formatted_topic_labels_string = get_formatted_topic_labels_str(topic_labels)

        chat_summary = get_summary(
            get_conversation_str(st.session_state["messages"])
        )

        # Put them in the database
        insert_data_in_db(formatted_msgs_str, formatted_topic_labels_string, chat_summary)

        show_report(topic_labels)

    # display_chat(st.session_state["user_id"], date)
    # new_chat()

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