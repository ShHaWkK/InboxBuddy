import streamlit as st
from openai import OpenAI
from config import OPENAI_API_KEY
from mail.imap import fetch_latest_mails
from database.db import save_mail
from core.core_agent import process_mail

client = OpenAI(api_key=OPENAI_API_KEY)

st.title("💬 InboxBuddy - Assistant IA Conversationnel")

if "history" not in st.session_state:
    st.session_state["history"] = []

# Assistant chat
user_input = st.chat_input("Pose une question sur tes mails...")

if user_input:
    st.session_state["history"].append({"role": "user", "content": user_input})
    messages = [{"role": h["role"], "content": h["content"]} for h in st.session_state["history"]]

    # Enrichir avec les derniers mails
    mails = fetch_latest_mails(3)
    mails_text = "\n".join([f"De: {m['from']}, Sujet: {m['subject']}, Body: {m['body'][:300]}" for m in mails])
    messages.insert(0, {"role": "system", "content": f"Voici les 3 derniers mails reçus :\n{mails_text}"})

    # Envoi à GPT
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages
    )
    answer = response.choices[0].message.content
    st.session_state["history"].append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)

for h in st.session_state["history"]:
    st.chat_message(h["role"]).write(h["content"])
