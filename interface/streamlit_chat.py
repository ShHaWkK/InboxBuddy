import streamlit as st
from openai import OpenAI
from config import OPENAI_API_KEY
from mail.imap import fetch_latest_mails

client = OpenAI(api_key=OPENAI_API_KEY)

st.title("💬 InboxBuddy - Chat Assistant IA")

if "history" not in st.session_state:
    st.session_state["history"] = []

user_input = st.chat_input("Pose une question sur tes mails...")

if user_input:
    st.session_state["history"].append({"role": "user", "content": user_input})

    mails = fetch_latest_mails(3)
    context = "\n".join([f"De: {m['from']}, Sujet: {m['subject']}, Body: {m['body'][:200]}" for m in mails])

    messages = [{"role": "system", "content": f"Voici les 3 derniers mails :\n{context}"}] + st.session_state["history"]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = response.choices[0].message.content
    st.session_state["history"].append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)

for h in st.session_state["history"]:
    st.chat_message(h["role"]).write(h["content"])
