import os
import json
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import openai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with AI Models!",
    page_icon=":brain:",
    layout="centered"
)

# Load API keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DATA = json.load(open(f"{WORKING_DIR}/config.json"))
OPENAI_API_KEY = CONFIG_DATA["OPENAI_API_KEY"]

# Configure APIs
gen_ai.configure(api_key=GOOGLE_API_KEY)
openai.api_key = OPENAI_API_KEY

# Set up the Google Gemini-Pro model
gemini_model = gen_ai.GenerativeModel('gemini-pro')

# Dropdown for selecting the model
selected_model = st.selectbox(
    "Choose the AI Model:",
    ["Google Gemini-Pro", "OpenAI GPT-4o"]
)

# Initialize chat session in Streamlit
if "gemini_chat_session" not in st.session_state:
    st.session_state.gemini_chat_session = gemini_model.start_chat(history=[])
if "openai_chat_history" not in st.session_state:
    st.session_state.openai_chat_history = []

# Chat Title
st.title(f"🤖 {selected_model} - ChatBot")

# Display chat history based on selected model
if selected_model == "Google Gemini-Pro":
    for message in st.session_state.gemini_chat_session.history:
        with st.chat_message("assistant" if message.role == "model" else "user"):
            st.markdown(message.parts[0].text)

elif selected_model == "OpenAI GPT-4o":
    for message in st.session_state.openai_chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input(f"Ask {selected_model}...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)

    if selected_model == "Google Gemini-Pro":
        # Send user's message to Gemini-Pro
        gemini_response = st.session_state.gemini_chat_session.send_message(user_prompt)
        st.chat_message("assistant").markdown(gemini_response.text)

    elif selected_model == "OpenAI GPT-4o":
        # Add user's message to OpenAI chat history
        st.session_state.openai_chat_history.append({"role": "user", "content": user_prompt})

        # Send user's message to GPT-4o
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                *st.session_state.openai_chat_history
            ]
        )
        assistant_response = response.choices[0].message.content
        st.session_state.openai_chat_history.append({"role": "assistant", "content": assistant_response})
        st.chat_message("assistant").markdown(assistant_response)
