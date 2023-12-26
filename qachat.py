from dotenv import load_dotenv
load_dotenv()  # Loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
def get_gemini_response(question):
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input section
input_text = st.text_input("Input: ", key="input")
submit_button = st.button("Ask the question")

# Input validation and handling
if submit_button and input_text:
    try:
        # Get Gemini response
        response = get_gemini_response(input_text)

        # Add user query and response to session state chat history
        st.session_state['chat_history'].append(("You", input_text))
        st.subheader("The Response is")
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))
    except Exception as e:
        st.error(f"Error: {e}")

# Display chat history
st.subheader("The Chat History is")
for role, text in st.session_state.get('chat_history', []):
    st.write(f"{role}: {text}")
