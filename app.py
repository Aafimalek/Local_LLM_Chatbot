import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="wide",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Add custom CSS for styling
st.markdown(
    """
    <style>
    .chat-message {
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        max-width: 80%;
        color: #000;  /* Ensure text is visible */
    }
    .user-message {
        background-color: #f1f1f1;
        align-self: flex-end;
    }
    .assistant-message {
        background-color: #e1f7d5;
        align-self: flex-start;
    }
    .sidebar .sidebar-content {
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar content
st.sidebar.title("Gemini Pro ChatBot")
st.sidebar.markdown("Welcome to the Gemini Pro ChatBot! Ask any questions you have, and Gemini Pro will assist you.")

# Clear chat button in the sidebar
if st.sidebar.button("Clear Chat"):
    st.session_state.chat_session = model.start_chat(history=[])
    st.rerun()

# Display the chatbot's title on the page
st.title("🤖 Gemini Pro - ChatBot")

# Display the chat history
for message in st.session_state.chat_session.history:
    role = translate_role_for_streamlit(message.role)
    message_class = "user-message" if role == "user" else "assistant-message"
    with st.chat_message(role):
        st.markdown(f'<div class="chat-message {message_class}">{message.parts[0].text}</div>', unsafe_allow_html=True)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(f'<div class="chat-message user-message">{user_prompt}</div>', unsafe_allow_html=True)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(f'<div class="chat-message assistant-message">{gemini_response.text}</div>', unsafe_allow_html=True)
