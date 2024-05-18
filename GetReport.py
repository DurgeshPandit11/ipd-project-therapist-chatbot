# define dependency 
from tensorflow.keras.models import load_model
import pickle
import nltk
import numpy as np
import pandas as pd
import random
from nltk.stem import WordNetLemmatizer

# load model
model = load_model('sent_clf_model_cc_data.keras')

# Load words
with open('words_in_all_patterns.pkl', 'rb') as file:
    words_in_all_patterns = pickle.load(file)

# Load tags
with open('all_tags.pkl', 'rb') as f:
    all_tags = pickle.load(f)

lemmatizer = WordNetLemmatizer()

def preprocess_user_message(user_message):
    # Tokenizing and lemmatizing user message
    words_in_user_message = nltk.word_tokenize(user_message)
    words_in_user_message = [lemmatizer.lemmatize(word.lower()) for word in words_in_user_message]

    # print("words_in_user_message:", words_in_user_message)

    # Converting user message to vector
    user_message_vector = [0] * len(words_in_all_patterns)
    
    # w: word in user input
    # word: word in the list of all words
    for w in words_in_user_message:
        for i, word in enumerate(words_in_all_patterns):
            if word == w:
                user_message_vector[i] = 1
    
    user_message_vector = np.array(user_message_vector)
    # print("User message vector:", user_message_vector)
    
    return user_message_vector

def predict_tag_for_user_message(user_message_vector):
    res = model.predict(np.array([user_message_vector]), verbose = 0)[0]
    ERROR_THRESHOLD = 0.4

    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key = lambda x: x[1], reverse = True)

    # returns all tags whose prob. > 0.25
    tag_and_probability = []
    for r in results:
        tag_and_probability.append({'intent': all_tags[r[0]], 'probability': str(r[1])})

    # print("tag_and_probability:", tag_and_probability)

    if len(tag_and_probability) != 0:
        return tag_and_probability
    else:
        return [{"intent": "unknown"}]

def get_user_messages(messages_dict_list: list):
    user_messages_list = []
    for msg_dict in messages_dict_list:
        if msg_dict["role"] == "user":
            user_messages_list.append(msg_dict["content"])
    return user_messages_list