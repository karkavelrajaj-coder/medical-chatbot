import streamlit as st
import google.generativeai as genai
import os

# Page config
st.set_page_config(
    page_title="Medical AI Chatbot",
    page_icon="🩺",
    layout="centered"
)

# Load API Key
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Medical system prompt
SYSTEM_PROMPT = """
You are a medical assistant chatbot.
- Provide general medical information only.
- Do NOT provide diagnosis.
- Always suggest consulting a qualified doctor.
- Be polite, clear, and professional.
"""

# UI
st.title("🩺 Medical AI Chatbot")
st.caption("Powered by AI | Educational use only")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)

# User input
user_input = st.chat_input("Ask a medical question...")

if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append(("user", user_input))

    # Generate response
    prompt = SYSTEM_PROMPT + "\nUser: " + user_input

    response = model.generate_content(prompt)
    bot_reply = response.text

    # Display bot message
    st.chat_message("assistant").markdown(bot_reply)
    st.session_state.chat_history.append(("assistant", bot_reply))

# Disclaimer
st.warning("⚠️ This chatbot does NOT replace professional medical advice.")
