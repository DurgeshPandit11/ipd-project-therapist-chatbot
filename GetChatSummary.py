from openai import OpenAI
import os

client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

def get_conversation_str(message_dict_list):
    conversation_str = ""
    for dict in message_dict_list[1:]:
        conversation_str += dict["role"] + ": " + dict["content"] + "\n"
    return conversation_str


def get_summary(conversation_str: str):
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages= [
            {"role": "system", "content": "Summarize this conversation between a therapist chatbot assistant and a client such that it can be used in the system message for the next seesion."}, 
            {"role": "user", "content": conversation_str}
        ]
    )

    return completion.choices[0].message.content