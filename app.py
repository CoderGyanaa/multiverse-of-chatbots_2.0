"""
app.py
The Multiverse of Chatbots — Streamlit + Gemini API
MirAI School of Technology | Virtual Summer Internship 2026
Assignment 3: The Memory Vault (Stateful Chatbot)

Upgraded from a stateless single-turn app to a stateful chat interface
using st.session_state, st.chat_message, and st.chat_input.
"""

import streamlit as st
from utils import PERSONAS, get_persona_names, ask_chatbot_with_history, ChatbotError

# ----------------------------------------------------------------
# Page Config + Styling
# ----------------------------------------------------------------
st.set_page_config(page_title="The Multiverse of Chatbots", page_icon="🌀", layout="centered")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ----------------------------------------------------------------
# API Initialization
# ----------------------------------------------------------------
DEFAULT_MODEL = "gemini-3.1-flash-lite"

# ----------------------------------------------------------------
# Task 1: Initialize the Memory Vault
# ----------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------------------------------------------
# Sidebar — API key, model, persona, and controls
# ----------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Setup")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Paste your key here",
        help="Get a free key at aistudio.google.com/apikey",
    )
    st.caption("🔑 Get a free key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)")

    model = st.selectbox(
        "Model",
        ["gemini-3.1-flash-lite", "gemini-3.5-flash"],
        index=0,
        help="Flash-Lite is cheapest with the highest free-tier limits. Flash is the flagship, more capable but pricier.",
    )

    st.markdown("---")
    persona_name = st.selectbox("Who do you want to talk to?", get_persona_names())

    st.markdown("---")
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# ----------------------------------------------------------------
# Header
# ----------------------------------------------------------------
st.markdown("<div class='mv-title'>The MULTIVERSE OF CHATBOTS</div>", unsafe_allow_html=True)
st.caption(f"Currently talking to: **{persona_name}**")

# ----------------------------------------------------------------
# Task 2: Render the Chat History
# ----------------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------------------------------------------------------
# Task 3: Upgrade the Input UI (st.chat_input + walrus operator)
# ----------------------------------------------------------------
if user_message := st.chat_input("Say something..."):

    if not api_key:
        st.error("Please add your Gemini API key in the sidebar.")
    else:
        # ----------------------------------------------------------------
        # Task 4: Save the user's message to memory, then render it
        # ----------------------------------------------------------------
        st.session_state.messages.append({"role": "user", "content": user_message})
        with st.chat_message("user"):
            st.markdown(user_message)

        # ----------------------------------------------------------------
        # Call Gemini with the FULL conversation so far, then save + render
        # the assistant's reply
        # ----------------------------------------------------------------
        with st.chat_message("assistant"):
            with st.spinner(f"{persona_name} is thinking..."):
                try:
                    response_text = ask_chatbot_with_history(
                        api_key, persona_name, st.session_state.messages, model=model
                    )
                    st.markdown(response_text)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response_text}
                    )
                except ChatbotError as e:
                    st.error(str(e))
