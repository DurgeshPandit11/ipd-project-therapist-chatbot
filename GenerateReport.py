import streamlit as st
import ModelWorking
import ChatbotApp # import get_session_messages
import matplotlib.pyplot as plt
# For HF Model
from transformers import pipeline

conversation = ChatbotApp.get_session_messages()

def get_user_messages(conversation: list):
    user_messages = []
    for dict in conversation:
        if dict["role"] == "user":
            user_messages.append(dict["content"])
    return user_messages

def get_labels(user_messages: list):
    labels_for_messages = []
    for message in user_messages:
        label = ModelWorking.predict_tag_for_user_message(
            ModelWorking.preprocess_user_message(message)
        )[0]["intent"]

        labels_for_messages.append(label)
    
    return labels_for_messages

topics = get_labels(get_user_messages(conversation))

fig = plt.figure(figsize=(2,1.5))
plt.xticks(rotation=50)
plt.xlabel("Topic")
plt.ylabel("Frequency")
plt.hist(
    [topic for topic in topics if topic != "unknown"]
)
st.pyplot(fig)

# HF Pretrained Model
hf_sentiment_classifier = pipeline("text-classification", model='bhadresh-savani/distilbert-base-uncased-emotion')

def get_hf_model_labels(user_messages: list):
    hf_labels_for_messages = []
    for message in user_messages:
        label = hf_sentiment_classifier(message)[0]["label"]
        hf_labels_for_messages.append(label)
    
    return hf_labels_for_messages

hf_model_sentiments = get_hf_model_labels(get_user_messages(conversation))

fig = plt.figure(figsize=(2,1.5))
plt.xlabel("Sentiment")
plt.ylabel("Frequency")
plt.hist(hf_model_sentiments)
st.pyplot(fig)

st.write(topics)
st.write(hf_model_sentiments)