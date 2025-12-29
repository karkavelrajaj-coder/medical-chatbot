import streamlit as st
from google import genai

# Page config
st.set_page_config(
    page_title="Medical AI Chatbot",
    page_icon="🩺",
    layout="centered"
)

# Initialize Gemini client (NEW SDK)
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

SYSTEM_PROMPT = """
You are a medical assistant chatbot.

Rules:
- Provide general medical information only
- Do NOT diagnose diseases
- Do NOT prescribe medication
- Always recommend consulting a licensed doctor
- Keep responses concise and professional
"""

st.title("🩺 Medical AI Chatbot")
st.caption("Powered by AI | Educational use only")

# Session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask a medical question...")

if user_input:
    # Store user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    st.chat_message("user").markdown(user_input)

    # Gemini call (NEW API)
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=SYSTEM_PROMPT + "\nUser: " + user_input
    )

    reply = response.text

    # Store assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
    st.chat_message("assistant").markdown(reply)

st.warning("⚠️ This chatbot does NOT replace professional medical advice.")
