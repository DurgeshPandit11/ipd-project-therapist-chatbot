import streamlit as st
from openai import OpenAI
import os

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
    if prompt := st.chat_input(): # disabled=st.session_state["session_ended"]
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
