import streamlit as st
from google import genai

# Streamlit page config
st.set_page_config(
    page_title="Medical AI Chatbot",
    page_icon="🩺",
    layout="centered"
)

# Initialize Gemini client using API key stored in Streamlit secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# System instructions
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

# Initialize session message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Accept user input
user_input = st.chat_input("Ask a medical question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    # Generate model response
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=SYSTEM_PROMPT + "\nUser: " + user_input
    )

    # Extract text
    reply = response.text

    # Add and display bot reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)

# Medical advice disclaimer
st.warning("⚠️ This chatbot does NOT replace professional medical advice.")
