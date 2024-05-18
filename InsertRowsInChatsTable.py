import streamlit as st
import json
import mysql.connector

conn = st.connection('mysql', type='sql')

ipd_db_conn = mysql.connector.connect(
    host="localhost",
	user="root",
	password="Mysql@123",
	database="ipd"
)

cursor = ipd_db_conn.cursor(buffered = True)

def insert_new_record_chats_table(userid: int, session_date: str, formatted_messages_str: str):
    query = 'INSERT INTO chats (user_id, chat_date, messages) VALUES ({}, "{}", "{}");'.format(userid, session_date, formatted_messages_str)
    cursor.execute(query)
    ipd_db_conn.commit()
    st.success("Success")

def format_message(messages_dict_list: list):
    messages_str = json.dumps(messages_dict_list)

    messages_str = messages_str.replace('"', '""')
    messages_str = messages_str.replace("'", "''")

    return messages_str

messages_dict_list = [
  {
    "role": "system",
    "content": "You are a therapist chatbot. The user will describe their feelings or situation to you. Respond to them as a therapist and continue the session by asking the next question whenever necessary."
  },
  {
    "role": "assistant",
    "content": "Welcome! How are you feeling today?"
  },
  {
    "role": "user",
    "content": "Hi. I've been struggling a lot lately. I just can't shake this feeling of emptiness and sadness."
  },
{
    "role": "assistant",
    "content": "Maybe if you start to reflect on what is going on in your life, especially any recent situations or decisions, you will start to feel more full.Since you're sad, most likely you need to be patient with how long this feeling lasts. Also, the feeling of emptiness can motivate you to find new situations and relationships to fill this in."
  },
  {
    "role": "user",
    "content": "I don't enjoy anything anymore. Even things I used to love doing just feel meaningless now. I feel exhausted all the time, and it's hard to even get out of bed in the morning."
  },
  {
    "role": "assistant",
    "content": "Maybe you are depressed.The good news about being depressed is that you can be aware of how you feel. This is the first step to finding new ways to be and new paths to go!"
  },
  {
    "role": "user",
    "content": "What do you mean?"
  },
  {
    "role": "assistant",
    "content": "Depression is a general term which describes a feeling of low energy and of being somewhat lost in direction of life. It is a very common feeling so people usually know what you mean when you say depression.What do you think would help you feel more secure in daily life?This is the direction to go, to understand and know your own particular reasons for feeling depressed, and to address these in a caring and kind way."
  },
  {
    "role": "user",
    "content": "Maybe getting enough sleep and improving my appetite can help me but some nights I can't sleep at all, and other nights I sleep too much and I just don't feel like eating anymore."
  },
  {
    "role": "assistant",
    "content": "Sleep and eating are two of the most basic ways of taking care of yourself. Since life is full of activity, some people require more sleep than others. And some people are so busy taking care of business that they forget to take care of themselves.If you'd like feeling more secure, pay close attention to your own needs and make sure your life includes plenty of time for rest and recuperation from all the daily and major living you do."
  },
  {
    "role": "user",
    "content": "Can you suggest some ways to improve my sleep and appetite?"
  },
  {
    "role": "assistant",
    "content": "If you're taking care of a lot of business and find yourself in a lot of stress then maybe your natural rhythm is to sleep and eat at odd times.If you're able to, then schedule your sleep and eating around the times which are the most conducive for your body to accept.Sleep is very much a part of feeling secure. Concentrate on getting enough sleep and if you're not able to do this, then for improving your appetite, offer yourself gentle foods such as fruit, yogurt, pudding, custard, whatever you feel would be good to eat.Even if you are not able to get more sleep, your body will appreciate the effort to have quality sleep."
  },
  {
    "role": "user",
    "content": "Thank you. I will try to follow some of that advise."
  },
  {
    "role": "assistant",
    "content": "Great! Let me know how you're doing, if you feel like sharing your results and if you would like suggestions on other ways to improve your sleep and appetite!"
  }
]

formatted_messages_str = format_message(messages_dict_list)
st.write(formatted_messages_str)

insert_new_record_chats_table(1, "2024-04-27", formatted_messages_str)



# Try: can also use: with conn.session as session: \n\tsession.execute(st.text(query)) \nsession.commit()