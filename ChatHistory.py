import streamlit as st

def show_chat_messages(messages: list, topic_labels: list, gen_sent_labels: list):
    j = 0
    for i in range(1, len(messages)):
        with st.chat_message(messages[i]["role"]):
            st.write(messages[i]["content"])
        if messages[i]["role"] == "user":
            st.write("Topic:", topic_labels[j])
            st.write("Emotion:", gen_sent_labels[j])
            j += 1

messages = [
  {
    "role": "system",
    "content": "You are a therapist chatbot. The user will describe their feelings or situation to you. Respond to them as a therapist and continue the session by asking the next question. Here is a summary of the previous session: Client has been struggling with feelings of emptiness, sadness, and exhaustion, finding it hard to enjoy activities they used to love. They mentioned trouble with sleep and appetite. Therapist provided support by acknowledging their feelings, suggesting reflection on recent situations, and focusing on self-care through rest and nutritious foods. Client expressed willingness to try the advice given and the therapist encouraged them to share their progress in the next session."
  },
  {
    "role": "assistant",
    "content": "Welcome! How are you feeling today?"
  },
  {
    "role": "user",
    "content": "Hi. I've been trying to implement some of the advice you gave me. It's been a bit of a mixed bag, to be honest."
  },
  {
    "role": "assistant",
    "content": "Good for you to keep trying to find answers to help your feelings!Sleep and appetite are classic areas of impact from depression.The best way to go may be to decide when you will address these areas since they are at the root of how you feel. And, if you're feeling unsure whether you'd like to try these suggestions, talk with a therapist who would be able to guide you in making the most of your current circumstance."
  },
  {
    "role": "user",
    "content": "Ok. I've been trying to stick to a regular sleep schedule, but some nights are still rough."
  },
  {
    "role": "assistant",
    "content": "Sleep and appetite are indeed classic areas of impact from depression.The good news is you're aware of how you feel. The unsureness is in whether you can change the way you feel in these areas and to what degree this is possible.Since you're in a difficult emotional place right now, reflect on the type of changes you'd like to make in your life and the possible paths to these changes.See if you can find a therapist who is a good match to your personality and style of interacting with others, and who has an interest in helping people to feel better.If you feel unsure of whether you'd like to make changes, reflect some more on your own and then try to find out who among your friends and family would be a good support for you at this time.Also, if you feel your depressed feelings are overwhelming you then this may be the time to open up to yourself and accept you're feeling down. This is a classic therapy formula which is very successful in clearing out old emotional clutter that someone may feel overwhelmed by, and in the end, feeling more relaxed and at ease with life."
  },
  {
    "role": "user",
    "content": "I understand. I will try to find someone to talk to about my feelings but as I mentioned, I am still not able to sleep well on nights. Can you help me with it?"
  },
  {
    "role": "assistant",
    "content": "Yes, definitely. A therapist is a good idea so you have time to reflect more deeply on your feelings than most people would be able to do while also being engaged in daily living.Also, if you're able to concentrate during the day then you may have an few more times of feeling down this week. Depressed feelings usually show more intensity in the feeling of being lost and not knowing what to do about it, than feeling down at night."
  },
  {
    "role": "user",
    "content": "I think I've been feeling a bit less exhausted, but the sadness and emptiness are still there. It's like I can't shake them no matter what I do."
  },
  {
    "role": "assistant",
    "content": "Maybe the best way to go would be to accept how you're feeling at the moment and to know you're feeling more than likely that the feelings will pass in a few days.Also, if you believe in a higher power then maybe this new belief is the one which is giving you the feeling of not being alone, even though at the moment you are alone.Also, there are many self-help groups which you can find online. Google \"self-help groups\" and you'll find plenty of probably very good advice and support from others who are in similar circumstances.Good luck!"
  },
  {
    "role": "user",
    "content": "Ok. I'll try to keep that in mind and search for self-help groups as well. It's just hard to imagine feeling happy again."
  },
  {
    "role": "assistant",
    "content": "How are you feeling in the midst of all the current awareness of how you're feeling?This may be a time of great learning and new awareness of who you are and what you'd like to do with your life."
  },
  {
    "role": "user",
    "content": "Like I mentioned earlier,  I've been feeling a bit less exhausted, but the sadness and emptiness are still there. It's like I can't shake them no matter what I do."
  },
  {
    "role": "assistant",
    "content": "Then maybe you are due for a new awareness of who you are and what you'd like to do with your life!Google is a good tool to find information about self-help groups. Some are very successful with people who have similar problems as you. Maybe you can find one and start to go to meetings."
  },
  {
    "role": "user",
    "content": "Ok. I'll try to do that"
  },
  {
    "role": "assistant",
    "content": "Good luck!"
  },
  {
    "role": "user",
    "content": "But can you also give me some advise regarding what to do to feel better?"
  },
  {
    "role": "assistant",
    "content": "Sure!Google is a great tool, but it's only a tool. If you're feeling sad and empty then probably you need to develop some new paths of thinking and interacting."
  },
  {
    "role": "user",
    "content": "What does that mean?"
  },
  {
    "role": "assistant",
    "content": "It is possible you're sad about something and don't know what it is.To feel sad is natural. To know the reason behind your sadness is a good sign of self-understanding and self-compassion."
  },
  {
    "role": "user",
    "content": "Ok. I'll try my best to find out the reason behind my sadness"
  },
  {
    "role": "assistant",
    "content": "Good luck in finding your answer!"
  }
]
topic_labels = [
  "parenting",
  "relationships",
  "relationships",
  "unknown",
  "depression",
  "unknown",
  "unknown",
  "unknown",
  "unknown",
  "depression"
]
gen_sent_labels = [
  "anger",
  "sadness",
  "joy",
  "sadness",
  "joy",
  "sadness",
  "joy",
  "joy",
  "anger",
  "joy"
]

show_chat_messages(messages, topic_labels, gen_sent_labels)